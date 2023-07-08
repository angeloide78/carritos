from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='carritos',
    version='1.0.0',
    author='Ángel Luis García García',
    author_email='angeluis78@email.com',
    description='Gestión de carritos de portátiles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/angeloide78/carritos',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'reportlab',
        'pyqt5',
    ],
    entry_points={
    'console_scripts': [
        'carritos = main:main',
    ],
    },
    classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    ],
)


