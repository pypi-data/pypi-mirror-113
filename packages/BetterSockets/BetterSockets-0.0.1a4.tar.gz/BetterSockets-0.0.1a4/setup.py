from setuptools import setup, find_packages
from BetterSockets import __version__

classifiers = \
    [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers ",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
]

setup(
    name="BetterSockets",
    version=__version__,
    description="Better Python sockets and asyncio streams",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Drageast/BetterSockets",
    author="Luca Michael Schmidt",
    author_email="schmidt.lucamichael@gmail.com",
    license="MIT",
    classifiers=classifiers,
    packages=find_packages(include=["BetterSockets", "BetterSockets.Asyncio.*", "BetterSockets.Threads.*", "BetterSockets.*"])
)
