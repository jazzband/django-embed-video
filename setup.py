from setuptools import setup, find_packages

import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')
CHANGES = read('CHANGES.rst')


setup(
    name='django-embed-video',
    packages=find_packages(),
    package_data={'embed_video': ['templates/embed_video/*.html']},
    use_scm_version=True,
    author='Cedric Carrard',
    author_email='cedric.carrard@gmail.com',
    url='https://github.com/jazzband/django-embed-video',
    description='Django app for easy embeding YouTube and Vimeo videos and music from SoundCloud.',
    long_description='\n\n'.join([README, CHANGES]),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=['youtube', 'vimeo', 'video', 'soundcloud'],
    install_requires=['requests >= 2.19', 'Django >= 1.11'],
    setup_requires=['nose', 'readme', 'setuptools_scm'],
    tests_require=['Django', 'requests >= 2.19', 'coverage'],
    test_suite='nose.collector',
)
