import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

package_name = "PyCMLutil"
version = "0.0.02"
authors = {"Principal Investigator": "Kenneth S. Campbell", 
            "Maintainer": "Hossein Sharifi"}
maintainer_email = "hossein.sharifi@uky.edu"
documentation_url = "https://github.com/Campbell-Muscle-Lab/PyCMLutilities"
install_requires = ['numpy>=1.16',
                    'pandas>=0.24',
                    'matplotlib>=3.0']
packages = setuptools.find_packages(exclude=("tests","demos"))
classifiers = [
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
python_requires = ">=3.6"

if __name__ == "__main__":
    
    import sys 
    if sys.version_info[:2] < (3, 6):
        raise RuntimeError("PyCMLutil requires python >= 3.6.")

    setuptools.setup(
        name=package_name,
        version=version,
        author=authors["Principal Investigator"],
        author_email=maintainer_email,
        description="A usefule python package for generating sientific figures.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=documentation_url,
        install_requires = install_requires,
        packages=packages,
        classifiers=classifiers,
        python_requires=python_requires,
    )
