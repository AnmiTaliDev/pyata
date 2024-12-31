# setup.py
from setuptools import setup, find_packages

setup(
    name="pyata",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'click>=7.0',     # Click для командной строки
        'zstandard>=0.15.0',  # Zstandard для сжатия данных
    ],
    entry_points={
        'console_scripts': [
            'pyata=pyata.ata:main',  # Создание консольной команды pyata
        ],
    },
    author="AnmiTaliDev",
    author_email="anmitali@anmitali.kz",
    description="AnmiTali Archive - Modern Terminal Archiver",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AnmiTaliDev/pyata",  # URL репозитория проекта
    keywords="archive, compression, cli",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: Utilities',
    ],
    python_requires=">=3.6",
)