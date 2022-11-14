from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

# Get admin.
admin = {}
with open("hvec_support/admin.py") as fp:
    exec(fp.read(), admin)

setup(
    name = 'hvec_support',
    version = admin['__version__'],
    author = admin['__author__'],
    author_email = admin['__author_email__'],
    description = 'Python package boosting conultancy work '
                'with Python, sqlite and excel.',
    long_description=long_description,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
        'Programming Language :: SQL',
        'Topic :: Scientific/Engineering'
    ],
    platforms='Windows',
    install_requires=['numpy>=1.17',
                      'matplotlib>=3.1',
                      'pandas>=1.5',
                      'scipy>=1.3',
                      'openpyxl>=3.0',
                      'tqdm>=4.0',
                      'requests>=2.0',
                      'datetime',
                      'easygui',
                      'openpyxl',
                      'matplotlib',
                      'hvec_importers @ git+https://github.com/HVEC-lab/hvec_importers'],
    packages=find_packages(exclude=[]),
)
