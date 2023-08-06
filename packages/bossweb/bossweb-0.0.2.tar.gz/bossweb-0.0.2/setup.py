import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# save requirements in a list 
REQUIREMENTS = open('requirements.txt').read().splitlines()

# This call to setup() does all the work
setup(
    name="bossweb",
    version="0.0.2",
    description="GUI framework to develop web and desktop apps in pure python using html, css and scripting. Powered by PyQt5, flask, Brython, selenium and libsass",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/atharva-naik/BossWeb",
    author="Atharva Naik",
    author_email="atharvanaik2018@gmail.com",
    license="GPL",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["BossWeb"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "runboss=BossWeb.__main__:main",
        ]
    },
)