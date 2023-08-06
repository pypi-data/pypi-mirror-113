from setuptools import setup, find_packages

setup(
    name             = 'oozie-api',
    version          = '1.2.0',
    description      = 'Python wrapper for Oozie Webservice REST API. Forked from oozie-webservice-api.',
    long_description = open('README.rst').read(),
    license          = 'MIT',
    author           = 'z1lv1n4s',
    author_email     = 'zilvinas.saltys@gmail.com',
    url              = 'https://github.com/zsaltys/oozie-webservice-api',
    download_url     = 'https://github.com/zsaltys/oozie-webservice-api/archive/master.zip',
    packages         = find_packages(exclude = ['test']),
    keywords         = ['oozie', 'webservice', 'api'],
    python_requires  = '>=2.6',
    classifiers=[
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
)
