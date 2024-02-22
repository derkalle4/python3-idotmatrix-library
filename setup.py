from pathlib import Path
from idotmatrix.version import __version__
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="idotmatrix",
    version=__version__,
    description="configure any iDotMatrix compatible 16x16 or 32x32 pixel display without the chinese iDotMatrix android / iOS app.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/derkalle4/python3-idotmatrix-library",
    author="Kalle Minkner",
    author_email="info@kalleminkner.de",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        "asyncio",
        "bleak",
        "pillow",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
