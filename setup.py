from setuptools import setup, find_packages

setup(
    name='Connection Leak cather service',
    version='0.1.0',
    description='This service is created for catching leak dabase connection.',
    author='Dipti Shirke',
    author_email='dptgawade@gmail.com',
    url='<URL>',
    install_requires=open('requirements.txt').read(),
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
)
