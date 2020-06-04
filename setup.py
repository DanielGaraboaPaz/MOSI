import setuptools

setuptools.setup(
    name='MOSI',
    version='0.1',
    author='Angel Daniel Garaboa Paz, Vicente Pérez Muñuzuri',
    author_email='angeldaniel.garaboa@usc.es',
    packages=['MOSI', 'docs'],
    license='GPLv3',
    url='https://github.com/DanielGaraboaPaz/MOSI',
    description='A python package for MetOcean data inquirer',
    long_description=open('README.rst').read(),
    install_requires=[
              "cdsapi",
              "argparse",
              "motuclient"
      ],
)
