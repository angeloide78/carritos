from setuptools import setup

setup(
    name="carritos",
    version="0.0.1",
    packages=["carritos"],
    entry_points={
        "console_scripts": [
            "carritos = carritos.__main__:main"
        ]
    },
    install_requires=["pyqt5"]
)
