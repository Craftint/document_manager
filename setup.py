from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in document_manager/__init__.py
from document_manager import __version__ as version

setup(
	name="document_manager",
	version=version,
	description="Document Manager",
	author="Dx",
	author_email="dx",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
