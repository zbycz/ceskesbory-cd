
from distutils.core import setup
import py2exe

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "1.0",
    description = "CD Ceske-sbory.cz",
    name = "cs-cd",

    options = {'py2exe': {'bundle_files': 3}},
    zipfile = 'runtime.dll',

    # targets to build
    windows = [
        {
            "script": "cs-cd.py", "icon_resources": [(1, "icon.ico")]
        }
    ]
)
