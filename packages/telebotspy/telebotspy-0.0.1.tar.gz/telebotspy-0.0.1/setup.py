from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Natural Language :: English',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
]

setup(
    name="telebotspy",
    version="0.0.1",
    author="US",
    author_email="author@example.com",
    description="A telegram bot package",
    long_description=open('README.md').read(),
    url = '',
    classifiers= classifiers,
    license = 'GPLv3',
    keywords = 'telegram',
    packages=find_packages(),
    python_requires=">=3.6",
)