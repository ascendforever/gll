


import setuptools
import Cython.Build
import pathlib


def recur(dir:pathlib.Path):
    for file in dir.iterdir():
        if file.is_dir():
            yield from recur(file)
        else:
            if file.suffix=='.pyx':
                yield file


setuptools.setup(
    name="gll",
    ext_modules=Cython.Build.cythonize(
        list(map(str, recur(pathlib.Path.cwd()))),
        nthreads=4,
        language=3
    ),
)








