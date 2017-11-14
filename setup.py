from setuptools import setup, find_packages

setup(
    name='block_id',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'click',
        'gunicorn',
        'requests'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'flask_testing'
    ],
)
