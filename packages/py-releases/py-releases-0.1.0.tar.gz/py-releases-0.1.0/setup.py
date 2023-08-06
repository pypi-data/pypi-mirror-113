from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='py-releases',
    packages=find_packages(include=['python_releases']),
    version='0.1.0',
    description='A package that get the avaliable python versions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuticoski/py-releases",
    author='Gr Kuticoski',
    license='GPL-2.0',
    data_files=[('releases_infos', ['python_releases/releases_infos/infos.json'])],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux"
    ],
    install_requires=[
        "beautifulsoup4==4.9.3",
        "requests==2.26.0"
    ]
)