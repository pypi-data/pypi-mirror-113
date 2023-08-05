"""
    artifact module to manage the download of salt artifacts
"""
import hashlib
import os
import re
import shutil
import sys
import tarfile
import tempfile
import urllib
import zipfile
from distutils.version import LooseVersion
from distutils.version import StrictVersion
from pathlib import Path

import aiohttp


async def fetch(hub, session, url, download=False, location=False):
    """
    Fetch a url and return json. If downloading artifact
    return the download location.
    """
    async with session.get(url) as resp:
        if resp.status == 200:
            if download:
                with open(location, "wb") as fn_:
                    fn_.write(await resp.read())
                return location
            return await resp.json()
        hub.log.critical(f"Cannot query url {url}. Returncode {resp.status} returned")
        return False


def verify_hash(hub, location, hash_value, hash_type):
    with open(location, "rb") as fp:
        file_hash = getattr(hashlib, hash_type)(fp.read()).hexdigest()
        if not file_hash == hash_value:
            return False
    return True


async def repo_data(hub):
    """
    Query repo.json file to gather the repo data
    """
    salt_repo_url = urllib.parse.urljoin(hub.OPT.heist.salt_repo_url, "repo.json")
    async with aiohttp.ClientSession() as session:
        data = await hub.artifact.salt.fetch(session, salt_repo_url)
        if not data:
            hub.log.critical(
                f"Query to {salt_repo_url} failed, falling back to"
                f"pre-downloaded artifacts"
            )
            return False
        return data


async def get(
    hub,
    target_os: str = "linux",
    version: str = "",
    repo_data: dict = None,
) -> str:
    """
    Download artifact if does not already exist.
    """
    artifact = [x for x in repo_data[version].keys() if target_os in x][0]
    verify_artifact = re.compile(f"salt-{version}.*{target_os}.*")
    if not verify_artifact.search(artifact):
        hub.log.error(f"The artifact {artifact} is not a valid Salt artifact")
        return False
    artifact_url = urllib.parse.urljoin(
        hub.OPT.heist.salt_repo_url, version + "/" + artifact
    )
    # TODO this needs to work for windows too
    # Ensure that artifact directory exists
    location = os.path.join(hub.OPT.heist.artifacts_dir, artifact)
    if not hub.tool.path.clean_path(hub.OPT.heist.artifacts_dir, artifact):
        hub.log.error(f"The {artifact} is not in the correct directory")
        return False

    # check to see if artifact already exists
    if hub.artifact.salt.latest("salt", version=version):
        hub.log.info(f"The Salt artifact {version} already exists")
        return location

    # download artifact
    async with aiohttp.ClientSession() as session:
        with tempfile.TemporaryDirectory() as tmpdirname:
            hub.log.info(
                f"Downloading the artifact {artifact} to {hub.OPT.heist.artifacts_dir}"
            )
            tmp_artifact_location = Path(tmpdirname) / artifact
            await hub.artifact.salt.fetch(
                session, artifact_url, download=True, location=tmp_artifact_location
            )
            if not hub.artifact.salt.verify_hash(
                tmp_artifact_location,
                hash_value=repo_data[version][artifact]["SHA3_512"],
                hash_type="sha3_512",
            ):
                hub.log.critical(f"Could not verify the hash of {location}")
                return False
            hub.log.info(f"Verified the hash of the {artifact} artifact")
            hub.log.info(
                f"Copying the the artifact {artifact} to {hub.OPT.heist.artifacts_dir}"
            )
            shutil.move(tmp_artifact_location, location)

    # ensure artifact was downloaded
    if not os.path.isdir(hub.OPT.heist.artifacts_dir):
        hub.log.critical(
            f"The target directory '{hub.OPT.heist.artifacts_dir}' does not exist"
        )
        return ""
    elif not any(version in x for x in os.listdir(hub.OPT.heist.artifacts_dir)):
        hub.log.critical(
            f"Did not find the {version} artifact in {hub.OPT.heist.artifacts_dir}."
            f" Untarring the artifact failed or did not include version"
        )
        return ""
    else:
        return location


def latest(hub, name: str, version: str = "") -> str:
    """
    Given the artifacts directory return the latest desired artifact

    :param str version: Return the artifact for a specific version.
    """
    names = []
    paths = {}
    if not os.path.isdir(hub.OPT.heist.artifacts_dir):
        return ""
    for fn in os.listdir(hub.OPT.heist.artifacts_dir):
        if fn.startswith(name):
            ver = fn.split("-")[1]
            names.append(ver)
            paths[ver] = fn
    names = sorted(names, key=LooseVersion)
    if version:
        if version in names:
            return os.path.join(hub.OPT.heist.artifacts_dir, paths[version])
        else:
            return ""
    elif not paths:
        return ""
    else:
        return os.path.join(hub.OPT.heist.artifacts_dir, paths[names[-1]])


async def deploy(
    hub,
    target_name: str,
    tunnel_plugin: str,
    run_dir: str,
    binary: str,
    target_os="linux",
    minion_id=None,
):
    """
    Deploy the salt minion to the remote system
    """
    root_dir = run_dir / "root_dir"
    binary_path = run_dir / "salt"
    conf_dir = root_dir / "conf"
    conf_tgt = conf_dir / "minion"

    if not hub.tool.path.clean_path(
        hub.heist.init.default(target_os, "run_dir_root"), run_dir
    ):
        hub.log.error(f"The path {binary_path} is not a valid path")
        return False

    if not hub.tool.path.clean_path(hub.OPT.heist.artifacts_dir, binary):
        hub.log.error(f"The path {binary} is not a valid path")
        return False

    config = hub.tool.config.mk_config(
        config=hub.tool.config.get_minion_opts(
            run_dir, target_name, target_os=target_os, minion_id=minion_id
        )
    )
    if not config:
        hub.log.error(
            "Could not create the minion configuration to copy to the target."
        )
        return False

    # create dirs and config
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"mkdir -p {conf_dir} {root_dir}"
    )
    if ret.returncode != 0 or ret.stderr:
        hub.log.error(f"Could not make {conf_dir} or {root_dir} on remote host")
        return False
    try:
        await hub.tunnel[tunnel_plugin].send(target_name, config, conf_tgt)
    except Exception as e:
        hub.log.error(str(e))
        hub.log.error(f"Failed to send {config} to {target_name} at {conf_tgt}")
    finally:
        if not sys.platform == "win32":
            os.remove(config)
    # Create tmp dir and unzip/untar the artifact and copy over
    hub.log.info(f"Preparing to ship salt to {root_dir}")

    if tarfile.is_tarfile(binary):
        with tempfile.TemporaryDirectory() as tmpdirname:
            salt_tar = tarfile.open(binary)
            salt_tar.extractall(tmpdirname)
            salt_tar.close()
            await hub.tunnel[tunnel_plugin].send(
                target_name, Path(tmpdirname) / "salt", run_dir, preserve=True
            )

    elif zipfile.is_zipfile(binary):
        with tempfile.TemporaryDirectory() as tmpdirname:
            salt_zip = zipfile.ZipFile(binary)
            salt_zip.extractall(tmpdirname)
            salt_zip.close()
            await hub.tunnel[tunnel_plugin].send(
                target_name, Path(tmpdirname) / "salt", run_dir, preserve=True
            )
    await hub.tunnel[tunnel_plugin].cmd(target_name, f"chmod +x {binary_path}")
    return binary_path
