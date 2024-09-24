from setuptools import setup
from blackcoinutils import __version__

#with open('requirements.txt') as f:
#    requirements = f.read().splitlines()

#install_reqs = parse_requirements('requirements.txt', session=False)
#requirements = [str(ir.req) for ir in install_reqs]

with open('README.rst') as readme:
    long_description = readme.read()

setup(name='blackoin-utils',
      version=__version__,
      description='Blackcoin utility functions',
      long_description=long_description,
      author='Konstantinos Karasavvas',
      author_email='kkarasavvas@gmail.com',
      url='https://github.com/BlackcoinDev/python-blackcoin-utils',
      license='MIT',
      keywords='blackcoin library utilities tools',
      install_requires=[
          'base58check>=1.0.2,<2.0',
          'ecdsa==0.18.0',
          'sympy>=1.2,<2.0',
          'python-bitcoinrpc>=1.0,<2.0',
          'hdwallet==2.2.1'
      ],
      packages=['bitcoinutils'],
      #package_data={
      #    'blackcoinutils': ['requirements.txt']
      #},
      #include_package_data=True,
      zip_safe=False
     )

