from setuptools import setup

from titulky import __version__


with open('README.md') as f:
    longDescription = f.read()


setup(
    author='Alexander Theler',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    description='Tiny SubRip subtitles editor',
    entry_points = {
        'console_scripts': [
            'titulky = titulky:main',
        ],
    },
    long_description=longDescription,
    long_description_content_type='text/markdown',
    name='titulky',
    project_urls={
        'GitHub': 'https://github.com/atheler/titulky',
        'Bug Tracker': 'https://github.com/atheler/titulky/issues',
    },
    py_modules=['titulky'],
    python_requires='>=3.6',
    url='http://pypi.org/project/titulky/',
    version=__version__,
)
