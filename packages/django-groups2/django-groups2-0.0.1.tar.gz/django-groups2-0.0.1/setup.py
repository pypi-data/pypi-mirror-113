#!/usr/bin/env python
from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

install_requires = [
    "Django>=3.0,<3.3",
    "django-treebeard>=4.2.0,<5.0,!=4.5",
]        

setup(
    name='django-groups2',
    version='0.0.1',
    description="An application for having better groups in Django",
    long_description=readme(),
    author='Serafeim Papastefanos',
    author_email='spapas@gmail.com',
    license='MIT',
    url='https://github.com/spapas/django-groups2/',
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),

    install_requires=install_requires,

    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
