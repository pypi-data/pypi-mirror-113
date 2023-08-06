from setuptools import find_packages, setup


setup(
    name='rolluptilelogs',
    version='0.0.1',
    author="Paul Norman",
    author_email="osm@paulnorman.ca",
    url="https://github.com/pnorman/rolluptilelogs",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Click',
        'numpy'
    ],
    setup_requires=[
        'flake8'
    ],
    entry_points={
        'console_scripts': ['rolluptilelogs=rolluptilelogs:cli']
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: GIS"
    ],
    python_requires="~=3.6"
)
