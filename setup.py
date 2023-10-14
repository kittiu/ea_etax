from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ea_etax/__init__.py
from ea_etax import __version__ as version

setup(
	name="ea_etax",
	version=version,
	description="EA\'s ETax Related Features",
	author="Ecosoft",
	author_email="kittiu@ecosoft.co.th",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
