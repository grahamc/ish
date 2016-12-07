from setuptools import setup, find_packages
setup(
    name='ish',
    scripts=['bin/ish'],
    package_dir={'ish': 'ish'},
    packages=find_packages(),
    install_requires=[
        'boto3==1.1.3',
        'jmespath==0.9.0'
    ]
)
