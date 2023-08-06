import omlet.utils as U


def get_gibson_config_path(fname: str):
    if not fname.endswith(".yaml"):
        fname += ".yaml"

    return U.resource_file_path("enlight.envs.gibson.config", fname)


def load_gibson_config(fname: str):
    return U.yaml_load(get_gibson_config_path(fname))


from .basic import *
