from setuptools import setup

setup(
    name="CLI Password Generator",
    version="1.0",
    author="Gabriel S.",
    packages=["src"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pwd-gen = src.generator:entry_point",
        ]
    },
)
