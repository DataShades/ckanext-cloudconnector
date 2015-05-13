from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-s3con',
    version=version,
    description="CKAN S3 connector for file uploading",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Sergey Motornyuk',
    author_email='sergey.motornyuk@linkdigital.com.au',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.s3con'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'boto',
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        s3con=ckanext.s3con.plugin:S3Plugin
    ''',
)
