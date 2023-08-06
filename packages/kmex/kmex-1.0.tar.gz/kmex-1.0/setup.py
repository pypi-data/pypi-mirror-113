import setuptools
from glob import glob

__package_name__ = "kmex"
__version__ = "1.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name=__package_name__,
    version=__version__,
    license='MIT',
    author="subhrajit mohanty",
    author_email="subhrajit.mohanty@katonic.ai",
    description="model explainability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=(
            "datasets",
            "examples",
            "notes"
            )
        ),
    include_package_data=True,
    python_requires='>=3.7, <4',
    install_requires = required
)