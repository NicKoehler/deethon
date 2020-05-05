import setuptools
import shutil
import os
import glob


CLEAN_FILES = ("./build", "./dist", "./*.egg-info")

for paths in CLEAN_FILES:
    paths = glob.glob(paths)
    for path in paths:
        print("removing", os.path.relpath(path))
        shutil.rmtree(path)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deethon",
    version="0.1.1",
    author="Aykut Yilmaz",
    author_email="aykuxt@gmail.com",
    description="Python3 library to easily download music from Deezer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aykuxt/deethon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["mutagen", "requests", "pycryptodome"],
    python_requires=">=3.6"
)
