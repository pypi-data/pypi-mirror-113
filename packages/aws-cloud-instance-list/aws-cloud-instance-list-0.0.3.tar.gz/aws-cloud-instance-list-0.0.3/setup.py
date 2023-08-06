from distutils.core import setup

setup(
    name="aws-cloud-instance-list",
    version="0.0.3",
    description="Aws cloud instance list",
    author="Kirill Shitikov",
    author_email="sh.kiruh@gmail.com",
    packages=["cloud_instance_list"],
    install_requires=[
        "click==8.0.1",
        "boto3==1.18.1",
        "requests==2.26.0",
        "tabulate==0.8.9"
    ],
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
