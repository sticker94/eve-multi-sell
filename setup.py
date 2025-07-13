# setup.py
from setuptools import setup

setup(
    name="eve-multi-sell",
    version="0.1.0",
    py_modules=["eve_multi_sell"],
    install_requires=["requests", "pyperclip"],
    entry_points={
        "console_scripts": [
            "eve-multi-sell=eve_multi_sell:main",
        ],
    },
)
