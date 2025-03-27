Python package to extract river centerline and water surface width estimation.

## Python Package: raster_medial_axis

## Project Structure:

raster_medial_axis/
├── raster_medial_axis/
│   ├── __init__.py
│   ├── medial_axis_processing.py
│   └── utils.py
├── tests/
│   ├── test_medial_axis.py
├── setup.py
├── README.md
└── LICENSE
## raster_medial_axis/medial_axis_processing.py

raster_medial_axis/__init__.py:

from .medial_axis_processing import process_raster_medial_axis

## setup.py:

from setuptools import setup, find_packages

setup(
    name='raster_medial_axis',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'rasterio',
        'scikit-image',
        'shapely',
        'geopandas'
    ],
    author='Pawan Thapa',
    author_email='pthapa2@gmail.com',
    description='Computes medial axis and width from raster images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/raster_medial_axis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

