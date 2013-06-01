import os

from setuptools import setup, find_packages

setup(
    name = 'django-embed-video',
    packages = find_packages(),
    version = '0.0.1',
    author = 'Juda Kaleta',
    author_email = 'juda.kaleta@gmail.com',
    url = '',
    description = 'Django template tags for YouTube and Vimeo',
    long_description = open('README').read(),
    classifiers = [
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topis :: Internet :: WWW/HTTP',
    ],
    keywords = ['youtube', 'vimeo', 'video'],
    test_suite = 'embed_video.tests.tests',
)
