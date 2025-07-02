#!/usr/bin/env python3
"""
Setup script for STForensicMacOS
"""

from setuptools import setup, find_packages
import os

# README dosyasını oku
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Requirements dosyasını oku
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="stforensicmacos",
    version="1.0.0",
    author="STForensic Team",
    author_email="contact@stforensic.com",
    description="MacOS Forensic Analysis Tool",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/silexi/stforensicmacos",
    project_urls={
        "Bug Tracker": "https://github.com/silexi/stforensicmacos/issues",
        "Documentation": "https://github.com/silexi/stforensicmacos#readme",
        "Source Code": "https://github.com/silexi/stforensicmacos",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Legal and Law Enforcement",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "stforensic=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yaml", "*.yml"],
    },
    keywords="forensic, analysis, macos, security, digital-forensics, incident-response",
    platforms=["macOS"],
    license="MIT",
    zip_safe=False,
) 