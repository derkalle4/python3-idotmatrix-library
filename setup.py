from setuptools import setup, find_packages

setup(
    name="idotmatrix",
    version="0.0.1",
    description="configure any iDotMatrix compatible 16x16 or 32x32 pixel display without the chinese iDotMatrix android / iOS app.",
    url="https://github.com/shuds13/pyexample",
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
