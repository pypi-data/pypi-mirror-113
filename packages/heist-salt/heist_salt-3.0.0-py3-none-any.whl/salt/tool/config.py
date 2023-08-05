import tempfile

import yaml


def get_minion_opts(hub, run_dir, target_name, target_os="linux", minion_id=None):
    config = {}
    roster = hub.heist.ROSTERS[target_name]
    if not hub.tool.path.clean_path(
        hub.heist.init.default(target_os, "run_dir_root"), run_dir
    ):
        hub.log.error(f"The {run_dir} directory is not valid")
        return False
    required = {
        "master": "127.0.0.1",
        "master_port": 44506,
        "publish_port": 44505,
        "root_dir": str(run_dir / "root_dir"),
        "id": minion_id,
    }
    minion_opts = roster.get("minion_opts")
    if minion_opts:
        for key, value in minion_opts.items():
            # Use configurations set by user
            config[key] = value

    for req in required.keys():
        if not config.get(req):
            config[req] = required[req]

    return config


def mk_config(hub, config):
    """
    Create a config to use with this execution and return the file path
    for said config
    """
    _, path = tempfile.mkstemp()
    with open(path, "w+") as wfp:
        yaml.safe_dump(config, wfp)
    return path
