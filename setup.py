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
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=["youtube", "vimeo", "video", "soundcloud"],
    python_requires=">=3.11",
    install_requires=[
        "requests >= 2.19",
        "Django >= 5.2",
    ],
    setup_requires=["readme", "setuptools_scm"],
    tests_require=["Django", "requests >= 2.19", "coverage"],
)
