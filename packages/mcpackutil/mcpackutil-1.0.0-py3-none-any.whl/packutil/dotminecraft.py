#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from pathlib import Path


def where() -> Path:
    system = platform.system().lower()

    temp = ""

    if system == "linux":
        temp = os.path.expanduser("~/.minecraft")
    elif system == "windows":
        temp = os.path.expandvars("%APPDATA%/.minecraft")
    elif system == "darwin":
        temp = os.path.expanduser("~/Library/Application Support/minecraft")

    return Path(temp)


versions = where() / "versions"

assets = where() / "assets"
assets_indexes = assets / "indexes"
assets_objects = assets / "objects"

resourcepacks = where() / "resourcepacks"

mod_loaders = ["forge", "liteloader", "rift", "fabric"]


def get_vanilla_packs():
    return (x.name for x in versions.glob("*") if x.is_dir() and not any(l in x.name for l in mod_loaders))
