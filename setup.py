from setuptools import setup, find_packages

setup(
    name='meta',
    version='0.1.0',
    include_package_data=True,
    install_requires=['asyncpg==0.18.3', 'aiohttp==3.5.4',
                      'uvloop==0.12.0', 'requests==2.21.0'],
    setup_requires=['pytest'],
    tests_require=['pytest', 'pytest-aiohttp==0.3.0'],
    packages=find_packages(),
)
