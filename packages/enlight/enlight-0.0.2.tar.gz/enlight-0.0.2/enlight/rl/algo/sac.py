import numpy as np
import torch
import torch.nn as nn
import torch.optim
import torch.nn.functional as F
from typing import Any, Union, Optional, Dict, List, ClassVar
import omlet.utils as U
from omlet.distributed import WorkerManager


class AlphaWrap(nn.Module):
    def __init__(self, init_temperature):
        super().__init__()
        self.log_alpha = nn.Parameter(
            torch.tensor(np.log(init_temperature)), requires_grad=True
        )

    @property
    def alpha(self):
        return self.log_alpha.exp()

    def forward(self, x):
        return self.alpha * x


class SAC(object):
    def __init__(
        self,
        *,
        actor: nn.Module,
        actor_update_freq: int = 2,
        actor_lr: Optional[float] = None,
        actor_optimizer: Optional[torch.optim.Optimizer] = None,
        action_range,
        action_shape,
        critic: nn.Module,
        critic_lr: Optional[float] = None,
        critic_optimizer: Optional[torch.optim.Optimizer] = None,
        critic_tau: float,
        critic_target_update_freq: int = 2,
        init_temperature: float,
        discount: float = 0.99,
        batch_size: int,
        log_alpha_lr: Optional[float] = None,
        log_alpha_optimizer: Optional[torch.optim.Optimizer] = None,
        target_entropy: Union[float, str] = "auto",
        manager: WorkerManager,
    ):
        """
        Args:
            actor_optimizer: if specified, LR will be ignored
        """
        self.manager = manager
        self.device = manager.device()
        self.actor = manager.data_parallel(actor, find_unused_parameters=True)
        self.critic_target = manager.data_parallel(
            U.clone_model(critic), find_unused_parameters=True
        )
        self.critic = manager.data_parallel(critic, find_unused_parameters=True)
        self.log_alpha = manager.data_parallel(AlphaWrap(init_temperature))

        # optimizers
        self.actor_optimizer = self._create_optimizer(
            self.actor.parameters(), actor_lr, actor_optimizer
        )
        self.critic_optimizer = self._create_optimizer(
            self.critic.parameters(), critic_lr, critic_optimizer
        )
        self.log_alpha_optimizer = self._create_optimizer(
            self.log_alpha.parameters(), log_alpha_lr, log_alpha_optimizer
        )

        if target_entropy == "auto":
            # heuristic: set target entropy to -|A|
            self.target_entropy = -np.prod(action_shape)
        else:
            self.target_entropy = float(target_entropy)

        self.discount = discount
        self.batch_size = batch_size
        self.actor_update_freq = actor_update_freq
        self.action_range = action_range
        self.critic_tau = critic_tau
        self.critic_target_update_freq = critic_target_update_freq

        self.train()
        self.critic_target.train()

    def train(self, training=True):
        self.training = training
        self.actor.train(training)
        self.critic.train(training)

    def _create_optimizer(self, params, lr, optimizer):
        if lr is None and optimizer is None:
            raise ValueError(
                "must specify either lr or torch.optim.Optimizer. "
                "If the latter is specified, lr will be ignored."
            )
        if optimizer is not None:
            return optimizer
        else:
            return torch.optim.Adam(params, lr=lr)

    @property
    def alpha(self):
        return self.manager.unwrap(self.log_alpha).alpha

    def act(self, obs, sample=False, vectorize=True):
        obs = torch.tensor(obs, dtype=torch.float32, device=self.device)
        if not vectorize:
            obs = obs.unsqueeze(0)
        # WARNING: this step is crucial to make DDP work
        # otherwise DDP throws error "Expected to have finished reduction in the prior
        # iteration before starting a new one. This error indicates that your module
        # has parameters that were not used in producing loss."
        dist = self.manager.unwrap(self.actor)(obs)
        action = dist.sample() if sample else dist.mean
        action = action.clamp(*self.action_range)
        assert action.ndim == 2 and action.size(0) == obs.size(0)
        return U.to_np(action)

    def update_critic(
        self,
        obs,
        obs_aug,
        action,
        reward,
        next_obs,
        next_obs_aug,
        not_done,
        logger,
        step,
    ):
        with torch.no_grad():
            # collate next_obs and next_obs_aug into one parallel CUDA call
            next_obs_collate = torch.cat([next_obs, next_obs_aug], dim=0)
            reward_collate = torch.cat([reward] * 2)
            not_done_collate = torch.cat([not_done] * 2)

            dist = self.actor(next_obs_collate)
            next_action = dist.rsample()
            log_prob = dist.log_prob(next_action).sum(-1, keepdim=True)
            target_Q1, target_Q2 = self.critic_target(next_obs_collate, next_action)
            target_V = torch.min(target_Q1, target_Q2) - self.alpha.detach() * log_prob
            target_Q = reward_collate + (not_done_collate * self.discount * target_V)
            # de-collate back to next_obs and next_obs_aug, average their Q value
            # to obtain a more robust estimate of target Q
            target_Q = sum(target_Q.chunk(2, dim=0)) / 2.

        # get current Q estimates
        obs_collate = torch.cat([obs, obs_aug], dim=0)
        action_collate = torch.cat([action] * 2, dim=0)
        # current_Q1 and current_Q2 are both [2*batch_size, 1]
        current_Q1, current_Q2 = self.critic(obs_collate, action_collate)
        # this is a 4x collate: Q1, Q2, Q1_aug, Q2_aug
        # all 4 computes MSE loss w.r.t. the same target Q
        current_Q_collate = torch.cat([current_Q1, current_Q2], dim=0)
        target_Q_collate = torch.cat([target_Q] * 4, dim=0)

        critic_loss = F.mse_loss(current_Q_collate, target_Q_collate)

        logger.log("train_critic/loss", critic_loss, step)

        # Optimize the critic
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        # self.critic.log(logger, step)

    def update_actor_and_alpha(self, obs, logger, step):
        # detach conv filters, so we don't update them with the actor loss
        dist = self.actor(obs, detach_encoder=True)
        action = dist.rsample()
        log_prob = dist.log_prob(action).sum(-1, keepdim=True)
        # detach conv filters, so we don't update them with the actor loss
        actor_Q1, actor_Q2 = self.critic(obs, action, detach_encoder=True)

        actor_Q = torch.min(actor_Q1, actor_Q2)

        actor_loss = (self.alpha.detach() * log_prob - actor_Q).mean()

        logger.log("train_actor/loss", actor_loss, step)
        logger.log("train_actor/target_entropy", self.target_entropy, step)
        logger.log("train_actor/entropy", -log_prob.mean(), step)

        # optimize the actor
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # self.actor.log(logger, step)

        self.log_alpha_optimizer.zero_grad()
        alpha_loss = (self.log_alpha((-log_prob - self.target_entropy).detach())).mean()
        logger.log("train_alpha/loss", alpha_loss, step)
        logger.log("train_alpha/value", self.alpha, step)
        alpha_loss.backward()
        self.log_alpha_optimizer.step()

    def update(self, replay_buffer, logger, step):
        batch = replay_buffer.sample(self.batch_size)
        obs = batch['obs']
        action = batch['action']
        reward = batch['reward']
        obs_next = batch['obs_next']
        not_done = batch['not_done']
        obs_aug = batch['obs_aug']
        obs_next_aug = batch['obs_next_aug']
        # print(obs.size(), action.size(), reward.size(), obs_next.size(), not_done.size())

        logger.log("train/batch_reward", reward.mean(), step)

        self.update_critic(
            obs, obs_aug, action, reward, obs_next, obs_next_aug, not_done, logger, step
        )

        if step % self.actor_update_freq == 0:
            self.update_actor_and_alpha(obs, logger, step)

        if step % self.critic_target_update_freq == 0:
            U.update_soft_params(self.critic, self.critic_target, self.critic_tau)
