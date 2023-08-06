def disable_gym_warnings(disable: bool = True):
    import gym, logging
    if disable:
        gym.logger.setLevel(logging.ERROR)
    else:
        gym.logger.setLevel(logging.WARNING)


from . import atari, wrappers
from .vec_env import *
from .ray_env import RayVectorEnv

disable_gym_warnings(True)