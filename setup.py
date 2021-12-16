import os
import platform
from setuptools import setup, Extension
import sysconfig

osname = platform.system()
paths = sysconfig.get_paths()
debug = True


def fill_template():
    with open("src/nativeInterop/cinterop/python.def.template") as fp:
        content = fp.read()
    formatted = content.format(INCLUDE_DIR=paths['platinclude'])
    with open("src/nativeInterop/cinterop/python.def", "w") as fp:
        fp.write(formatted)


def build_gradle():
    if osname == "Linux":
        if os.waitstatus_to_exitcode(os.system("./gradlew build")) != 0:
            raise Exception("Build failed")
    else:
        raise NotImplementedError(osname)


def extensions():
    folder = "debugStatic" if debug else "releaseStatic"

    native = Extension('kaudio',
                       sources=['src/nativeMain/cpp/entrypoint.cpp'],
                       include_dirs=[f"build/bin/native/{folder}/"],
                       library_dirs=[f"build/bin/native/{folder}/"],
                       libraries=["kaudio_python"])

    return [native]


fill_template()
build_gradle()

setup(
    name='kaudio',
    version='1.0',
    description='Python wrapper for kaudio',
    ext_modules=extensions()
)
