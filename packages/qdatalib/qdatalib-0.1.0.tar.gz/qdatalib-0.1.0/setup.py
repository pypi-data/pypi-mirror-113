"""
Installs the qdatalib package
"""

from setuptools import setup, find_packages
from pathlib import Path

import versioneer

readme_file_path = Path(__file__).absolute().parent / "README.md"

required_packages = ['pymongo', ' dnspython', 'qcodes>=0.25']
package_data = {"qdatalib": ["conf/telemetry.ini"] }


setup(
    name="qdatalib",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    python_requires=">=3.7",
    install_requires=required_packages,
    author= "Rasmus Bjerregaard Christensen",
    author_email="rbcmail@gmail.com",
    description="Library for Quantum Data file Organization",
    long_description=readme_file_path.open(encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="",
    package_data=package_data,
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
    ],
)
