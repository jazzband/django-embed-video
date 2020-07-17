#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="django-embed-video",
    packages=find_packages(),
    package_data={"embed_video": ["templates/embed_video/*.html"]},
    use_scm_version=True,
    author="Cedric Carrard",
    author_email="cedric.carrard@gmail.com",
    url="https://github.com/jazzband/django-embed-video",
    description="Django app for easy embedding YouTube and Vimeo videos and music from SoundCloud.",
    long_description="\n".join(
        [
            open("README.rst", encoding="utf-8").read(),
            open("CHANGES.rst", encoding="utf-8").read(),
        ]
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=["youtube", "vimeo", "video", "soundcloud"],
    install_requires=["requests >= 2.19", "Django >= 2.2"],
    setup_requires=["readme", "setuptools_scm"],
    tests_require=["Django", "requests >= 2.19", "coverage"],
)
