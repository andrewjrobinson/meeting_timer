
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="meeting_timer",
    version="0.3.0",
    author="Andrew Robinson",
    author_email="andrewjrobinson+mt@gmail.com",
    description="A simple application to allow you to keep your meetings or webinars running on time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewjrobinson/meeting_timer",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={  # Optional
        'console_scripts': [
            'meeting-timer=meeting_timer.main:main',
        ],
    },
    install_requires=[
#         'numpy',
    ],
)
