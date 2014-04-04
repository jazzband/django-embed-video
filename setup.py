from setuptools import setup, find_packages

import os

embed_video = __import__('embed_video')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')
CHANGES = read('CHANGES.rst')


setup(
    name='django-embed-video',
    packages=find_packages(),
    package_data={'embed_video': ['templates/embed_video/*.html']},
    version=embed_video.get_version(),
    author='Juda Kaleta',
    author_email='juda.kaleta@gmail.com',
    url='https://github.com/yetty/django-embed-video',
    description=embed_video.__doc__.strip(),
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=['youtube', 'vimeo', 'video', 'soundcloud'],
    install_requires=['requests >= 1.2.3', 'Django >= 1.5'],
    test_suite='nose.collector',
)
