import setuptools
from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="aws-cloud-instance-list",
    version="0.0.1",
    description="Aws cloud instance list",
    author="Kirill Shitikov",
    author_email="sh.kiruh@gmail.com",
    packages=setuptools.find_packages(where="cloud_instance_list"),
    install_requires=required,
    extras_require={
        'dev': [
            'pytest',
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={
        "console_scripts": ["cloud-instance-list=cloud_instance_list.main:info"],
    },
    url='https://github.com/shitikovkirill/aws-cloud-instance-list',
    download_url='https://github.com/shitikovkirill/aws-cloud-instance-list/archive/refs/heads/main.zip',
)
