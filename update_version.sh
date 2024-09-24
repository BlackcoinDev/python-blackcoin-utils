pip uninstall -y blackcoin-utils
python setup.py sdist bdist_wheel
pip install dist/blackcoin-utils-0.7.1.tar.gz
