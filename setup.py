from setuptools import setup, find_packages

setup(
    name='BYtDl',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'yt-dlp',
        'textual',
        'rich-pixels'
    ],
    entry_points={
        'console_scripts': [
            'bytdl=BYtDl.BYtDl:main',
        ],
    },
    author='0300dbdd1b',
    author_email='_@_',
    description='yt-dlp with a Textual interface.',
    url='https://github.com/0300dbdd1b/BYtDl',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
