#!/usr/bin/env python
from setuptools import setup, find_packages

# import sys
# import importlib
# importlib.reload(sys)
# reload(sys)
# sys.setdefaultencoding('utf-8')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="i61-sentry-dingtalk",
    version='0.1.1',
    author='sankyutang',
    author_email='tangjunkai@61info.cn',
    description='A Sentry extension which send errors stats to i61 DingTalk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='sentry dingtalk',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sentry_dingding = sentry_dingding.plugin:DingDingPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ]
)