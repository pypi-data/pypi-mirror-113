from setuptools import setup, find_packages

setup(
    name = 'shawlTrie',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = ['shawlTrie', 'pymongo'],
    entry_points = {
        'console_scripts': [
            'shawlTrie = shawlTrie.__main__:main'
        ]
    })