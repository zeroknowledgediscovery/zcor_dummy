import json
from setuptools import setup, find_packages

# Load project configuration from config.json
with open("setup.json", "r") as f:
    config = json.load(f)

# Use the loaded configurations in the setup
setup(
    name=config["name"],
    version=config["version"],
    description=config["description"],
    packages=find_packages(include=config["included_packages"]),
    install_requires=config["install_requires"],
    include_package_data=True
)