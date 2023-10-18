import os
import json
from setuptools import setup, find_packages

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

# Load project configuration from config.json
with open("setup.json", "r") as f:
    config = json.load(f)

assets_folder = package_files('zcor_dummy/ASSETS')

# Use the loaded configurations in the setup
setup(
    name=config["name"],
    version=config["version"],
    description=config["description"],
    packages=find_packages(include=config["included_packages"]),
    install_requires=config["install_requires"],
    package_data={
        'zcor_dummy': assets_folder,
    },
    include_package_data=True
)