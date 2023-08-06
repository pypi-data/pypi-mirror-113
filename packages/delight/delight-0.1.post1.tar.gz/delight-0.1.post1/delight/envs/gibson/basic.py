import os
from typing import Optional

from gibson2.envs.locomotor_env import (
    NavigateEnv,
    NavigateRandomEnv,
    NavigateRandomEnvSim2Real,
)
from .nav import NavigateRandomEnv2  # GPS + Compass: [d, cos(theta), sin(theta)]

from . import load_gibson_config
from ..wrappers import TimeLimit, FrameStack
from .wrappers import *
from omlet.distributed import get_cuda_visible_devices


GIBSON_ENV_VAR = "GIBSON_DEVICE_ID"


def make_gibson_basic(
    config_file,
    env_type="gibson",
    sim2real_track="static",
    modality=("rgb", "sensor"),
    single_modality_obs: bool = False,
    env_mode="headless",
    action_timestep=1.0 / 5.0,
    physics_timestep=1.0 / 40.0,
    device_idx: Optional[int] = None,
    random_position=False,
    random_height=False,
    rgb_to_int: bool = True,
    frame_stack: int = 3,
):
    """
    Args:
        device_idx: if None, read from CUDA_VISIBLE_DEVICES or GIBSON_DEVICE_ID
    """
    # FIXME: multi-modality doesn't work with FrameStack
    if single_modality_obs:
        if not isinstance(modality, str):
            assert len(modality) == 1
            modality = modality[0]
            assert isinstance(modality, str)

    if device_idx is None:
        if GIBSON_ENV_VAR in os.environ:
            device_idx = int(os.environ[GIBSON_ENV_VAR])
        else:
            visible_devices = get_cuda_visible_devices()
            if visible_devices:
                device_idx = visible_devices[0]
            else:
                device_idx = 0

    config_dict = load_gibson_config(config_file)
    if modality:
        config_dict["output"] = modality

    if env_type == "gibson":
        if random_position:
            env = NavigateRandomEnv2(
                config_file=config_dict,
                mode=env_mode,
                action_timestep=action_timestep,
                physics_timestep=physics_timestep,
                device_idx=device_idx,
                random_height=random_height,
            )
        else:
            env = NavigateEnv(
                config_file=config_dict,
                mode=env_mode,
                action_timestep=action_timestep,
                physics_timestep=physics_timestep,
                device_idx=device_idx,
            )
    elif env_type == "gibson_sim2real":
        env = NavigateRandomEnvSim2Real(
            config_file=config_dict,
            mode=env_mode,
            action_timestep=action_timestep,
            physics_timestep=physics_timestep,
            device_idx=device_idx,
            track=sim2real_track,
        )
    else:
        assert False, "unknown env_type: {}".format(env_type)

    env = TimeLimit(env, max_episode_steps=env.max_step)
    env = GibsonHWC2CHW(env)
    if rgb_to_int:
        env = GibsonRGBFloat2Int(env)
    if single_modality_obs:
        env = SingleModality(env, modality)
    if frame_stack and frame_stack > 0:
        env = FrameStack(env, k=frame_stack, generate_obs_space=False)
    return env


def make_gibson_debug(
    modality=("rgb", "sensor"),
    device_idx: Optional[int] = None,
    env_mode: str = "headless",
    rgb_to_int: bool = True,
    frame_stack: int = 3,
):
    return make_gibson_basic(
        "turtlebot_p2p_nav_fixed.yaml",
        env_type="gibson",
        modality=modality,
        env_mode=env_mode,
        device_idx=device_idx,
        random_position=False,
        random_height=False,
        rgb_to_int=rgb_to_int,
        frame_stack=frame_stack,
        single_modality_obs=(modality == "rgb"),
    )
