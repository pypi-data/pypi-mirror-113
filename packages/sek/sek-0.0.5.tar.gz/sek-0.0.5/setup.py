from setuptools import setup

setup(
    name='sek',
    version='0.0.5',
    author="Nick Gibbon",
    py_modules=["sek"],
    package_dir={'': 'src'},
)

setup(
    name='sek',
    entry_points={
        'console_scripts': [
            'sek = src.sek:main',
        ],
    }
)
