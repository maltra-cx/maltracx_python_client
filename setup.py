import os
from setuptools import setup

# maltracx
# Official maltra.cx REST API client


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="maltracx",
    version="0.0.1",
    description="Official maltra.cx REST API client",
    author="Johan Nestaas",
    author_email="johan@maltra.cx",
    license="BSD",
    keywords="",
    url="https://github.com/maltra-cx/maltracx_python_client",
    packages=['maltracx'],
    package_dir={'maltracx': 'maltracx'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'maltracx=maltracx:main',
        ],
    },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={
    #     'maltracx': ['templates/*.html'],
    # },
    # include_package_data=True,
)
