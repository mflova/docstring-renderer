"""Setups the python module."""

from setuptools import find_packages, setup

setup(
    name="docstring_renderer",
    version="0.0.1",
    maintainer="mflova",
    maintainer_email="mflovaa@gmail.com",
    python_requires=">=3.8",
    packages=find_packages(),
    platforms=["Linux"],
    install_requires=[],
    extras_require={
        "dev": [
            "flake8",
            "mypy",
            "black",
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "docstring_renderer=docstring_renderer.scripts.main:main",
        ]
    },
    zip_safe=False,
)
