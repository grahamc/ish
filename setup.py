from setuptools import setup, find_packages
setup(
    name='ish',
    scripts=['bin/ish'],
    package_dir={'ish': 'ish'},
    packages=find_packages(),
    install_requires=['boto3']
)
