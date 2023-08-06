import collections
import os
import gym
import numpy as np
from abc import ABC, abstractmethod
from multiprocessing import Process, Pipe
from typing import List, Tuple, Union, Optional, Callable, Dict, Any
import enlight.envs
import omlet.utils as U

try:
    import ray
except ImportError:
    pass


import cloudpickle


class CloudpickleWrapper(object):
    """A cloudpickle wrapper used in env.SubprocVectorEnv"""

    def __init__(self, data):
        self.data = data

    def __getstate__(self):
        return cloudpickle.dumps(self.data)

    def __setstate__(self, data):
        self.data = cloudpickle.loads(data)


class BaseVectorEnv(ABC, gym.Wrapper):
    """Base class for vectorized environments wrapper. Usage:
    ::

        env_num = 8
        envs = VectorEnv([lambda: gym.make(task) for _ in range(env_num)])
        assert len(envs) == env_num

    It accepts a list of environment generators. In other words, an environment
    generator ``efn`` of a specific task means that ``efn()`` returns the
    environment of the given task, for example, ``gym.make(task)``.

    All of the VectorEnv must inherit :class:`~tianshou.env.BaseVectorEnv`.
    Here are some other usages:
    ::

        envs.seed(2)  # which is equal to the next line
        envs.seed([2, 3, 4, 5, 6, 7, 8, 9])  # set specific seed for each env
        obs = envs.reset()  # reset all environments
        obs = envs.reset([0, 5, 7])  # reset 3 specific environments
        obs, rew, done, info = envs.step([1] * 8)  # step synchronously
        envs.render()  # render all environments
        envs.close()  # close all environments
    """

    def __init__(self, env_fns: List[Callable[[], gym.Env]]) -> None:
        self._env_fns = env_fns
        self.num_envs = len(env_fns)

    def __len__(self) -> int:
        """Return len(self), which is the number of environments."""
        return self.num_envs

    @abstractmethod
    def reset(self, id: Optional[Union[int, List[int]]] = None):
        """Reset the state of all the environments and return initial
        observations if id is ``None``, otherwise reset the specific
        environments with given id, either an int or a list.
        """
        pass

    @abstractmethod
    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Run one timestep of all the environments’ dynamics. When the end of
        episode is reached, you are responsible for calling reset(id) to reset
        this environment’s state.

        Accept a batch of action and return a tuple (obs, rew, done, info).

        :param numpy.ndarray action: a batch of action provided by the agent.

        :return: A tuple including four items:

            * ``obs`` a numpy.ndarray, the agent's observation of current \
                environments
            * ``rew`` a numpy.ndarray, the amount of rewards returned after \
                previous actions
            * ``done`` a numpy.ndarray, whether these episodes have ended, in \
                which case further step() calls will return undefined results
            * ``info`` a numpy.ndarray, contains auxiliary diagnostic \
                information (helpful for debugging, and sometimes learning)
        """
        pass

    @abstractmethod
    def seed(self, seed: Optional[Union[int, List[int]]] = None) -> None:
        """Set the seed for all environments. Accept ``None``, an int (which
        will extend ``i`` to ``[i, i + 1, i + 2, ...]``) or a list.
        """
        pass

    @abstractmethod
    def render(self, **kwargs) -> None:
        """Render all of the environments."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close all of the environments."""
        pass


class DummyVectorEnv(BaseVectorEnv):
    """Dummy vectorized environment wrapper, implemented in for-loop.
    """

    def __init__(self, env_fns: List[Callable[[], gym.Env]]) -> None:
        super().__init__(env_fns)
        self.envs = [e() for e in env_fns]

    def reset(self, id: Optional[Union[int, List[int]]] = None) -> None:
        if id is None:
            self._obs = np.stack([e.reset() for e in self.envs])
        else:
            if np.isscalar(id):
                id = [id]
            for i in id:
                self._obs[i] = self.envs[i].reset()
        return self._obs

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        assert len(action) == self.num_envs
        result = [e.step(a) for e, a in zip(self.envs, action)]
        self._obs, self._rew, self._done, self._info = zip(*result)
        self._obs = np.stack(self._obs)
        self._rew = np.stack(self._rew)
        self._done = np.stack(self._done)
        self._info = np.stack(self._info)
        return self._obs, self._rew, self._done, self._info

    def seed(self, seed: Optional[Union[int, List[int]]] = None) -> None:
        if np.isscalar(seed):
            seed = [seed + _ for _ in range(self.num_envs)]
        elif seed is None:
            seed = [seed] * self.num_envs
        result = []
        for e, s in zip(self.envs, seed):
            if hasattr(e, "seed"):
                result.append(e.seed(s))
        return result

    def render(self, **kwargs) -> None:
        result = []
        for e in self.envs:
            if hasattr(e, "render"):
                result.append(e.render(**kwargs))
        return result

    def close(self) -> None:
        return [e.close() for e in self.envs]


def _subproc_env_worker(
    parent,
    p,
    env_fn_wrapper,
    disable_gym_warnings: bool,
    gpu_idx: Optional[int],
    os_envs: Optional[Dict[str, Any]],
):
    if disable_gym_warnings:
        enlight.envs.disable_gym_warnings()
    if gpu_idx is not None:
        assert gpu_idx >= 0
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_idx)
    if os_envs is not None:
        assert isinstance(os_envs, collections.abc.Mapping)
        U.set_os_envs(os_envs)

    parent.close()
    env = env_fn_wrapper.data()
    try:
        while True:
            cmd, data = p.recv()
            if cmd == "step":
                p.send(env.step(data))
            elif cmd == "reset":
                p.send(env.reset())
            elif cmd == "close":
                p.send(env.close())
                p.close()
                break
            elif cmd == "render":
                p.send(env.render(**data) if hasattr(env, "render") else None)
            elif cmd == "seed":
                p.send(env.seed(data) if hasattr(env, "seed") else None)
            else:
                p.close()
                raise NotImplementedError
    except KeyboardInterrupt:
        p.close()


class SubprocVectorEnv(BaseVectorEnv):
    """Vectorized environment wrapper based on subprocess.

    .. seealso::

        Please refer to :class:`~tianshou.env.BaseVectorEnv` for more detailed
        explanation.
    """

    def __init__(
        self,
        env_fns: List[Callable[[], gym.Env]],
        obs_dtype=None,
        reward_dtype=None,
        done_dtype=None,
        disable_gym_warnings: bool = True,
        gpu_idx: Optional[Union[int, List[int]]] = None,
        os_envs: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(env_fns)
        self.closed = False
        self._dtypes = {"obs": obs_dtype, "reward": reward_dtype, "done": done_dtype}
        self.parent_remote, self.child_remote = zip(
            *[Pipe() for _ in range(self.num_envs)]
        )
        if isinstance(gpu_idx, (list, tuple)):
            assert (
                len(gpu_idx) == self.num_envs
            ), f"list of gpu_idx {gpu_idx} must match number of envs"
        else:
            gpu_idx = [gpu_idx] * self.num_envs
        self.processes = [
            Process(
                target=_subproc_env_worker,
                args=(
                    parent,
                    child,
                    CloudpickleWrapper(env_fn),
                    disable_gym_warnings,
                    gpu_i,
                    os_envs,
                ),
                daemon=True,
            )
            for (parent, child, env_fn, gpu_i) in zip(
                self.parent_remote, self.child_remote, env_fns, gpu_idx
            )
        ]
        for p in self.processes:
            p.start()
        for c in self.child_remote:
            c.close()

    def _convert_type(self, value, name):
        assert name in self._dtypes, "INTERNAL"
        dt = self._dtypes[name]
        if dt is None:
            return value
        else:
            return value.astype(dt)

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        assert len(action) == self.num_envs
        for p, a in zip(self.parent_remote, action):
            p.send(["step", a])
        result = [p.recv() for p in self.parent_remote]
        self._obs, self._rew, self._done, self._info = zip(*result)
        self._obs = self._convert_type(np.stack(self._obs), "obs")
        self._rew = self._convert_type(np.stack(self._rew), "reward")
        self._done = self._convert_type(np.stack(self._done), "done")
        return self._obs, self._rew, self._done, self._info

    def reset(self, id: Optional[Union[int, List[int]]] = None) -> None:
        if id is None:
            for p in self.parent_remote:
                p.send(["reset", None])
            self._obs = np.stack([p.recv() for p in self.parent_remote])
            self._obs = self._convert_type(self._obs, "obs")
        else:
            if np.isscalar(id):
                id = [id]
            for i in id:
                self.parent_remote[i].send(["reset", None])
            for i in id:
                self._obs[i] = self._convert_type(self.parent_remote[i].recv(), "obs")

        return self._obs

    def seed(self, seed: Optional[Union[int, List[int]]] = None) -> None:
        if np.isscalar(seed):
            seed = [seed + _ for _ in range(self.num_envs)]
        elif seed is None:
            seed = [seed] * self.num_envs
        for p, s in zip(self.parent_remote, seed):
            p.send(["seed", s])
        return [p.recv() for p in self.parent_remote]

    def render(self, **kwargs) -> None:
        for p in self.parent_remote:
            p.send(["render", kwargs])
        return [p.recv() for p in self.parent_remote]

    def close(self) -> None:
        if self.closed:
            return
        for p in self.parent_remote:
            p.send(["close", None])
        result = [p.recv() for p in self.parent_remote]
        self.closed = True
        for p in self.processes:
            p.join()
        return result


class RayVectorEnv(BaseVectorEnv):
    """Vectorized environment wrapper based on
    `ray <https://github.com/ray-project/ray>`_. However, according to our
    test, it is about two times slower than
    :class:`~tianshou.env.SubprocVectorEnv`.

    .. seealso::

        Please refer to :class:`~tianshou.env.BaseVectorEnv` for more detailed
        explanation.
    """

    def __init__(self, env_fns: List[Callable[[], gym.Env]]) -> None:
        super().__init__(env_fns)
        try:
            if not ray.is_initialized():
                ray.init()
        except NameError:
            raise ImportError(
                "Please install ray to support RayVectorEnv: pip3 install ray"
            )
        self.envs = [
            ray.remote(gym.Wrapper).options(num_cpus=0).remote(e()) for e in env_fns
        ]

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        assert len(action) == self.num_envs
        result = ray.get([e.step.remote(a) for e, a in zip(self.envs, action)])
        self._obs, self._rew, self._done, self._info = zip(*result)
        self._obs = np.stack(self._obs)
        self._rew = np.stack(self._rew)
        self._done = np.stack(self._done)
        self._info = np.stack(self._info)
        return self._obs, self._rew, self._done, self._info

    def reset(self, id: Optional[Union[int, List[int]]] = None) -> None:
        if id is None:
            result_obj = [e.reset.remote() for e in self.envs]
            self._obs = np.stack(ray.get(result_obj))
        else:
            result_obj = []
            if np.isscalar(id):
                id = [id]
            for i in id:
                result_obj.append(self.envs[i].reset.remote())
            for _, i in enumerate(id):
                self._obs[i] = ray.get(result_obj[_])
        return self._obs

    def seed(self, seed: Optional[Union[int, List[int]]] = None) -> None:
        if not hasattr(self.envs[0], "seed"):
            return
        if np.isscalar(seed):
            seed = [seed + _ for _ in range(self.num_envs)]
        elif seed is None:
            seed = [seed] * self.num_envs
        return ray.get([e.seed.remote(s) for e, s in zip(self.envs, seed)])

    def render(self, **kwargs) -> None:
        if not hasattr(self.envs[0], "render"):
            return
        return ray.get([e.render.remote(**kwargs) for e in self.envs])

    def close(self) -> None:
        return ray.get([e.close.remote() for e in self.envs])
