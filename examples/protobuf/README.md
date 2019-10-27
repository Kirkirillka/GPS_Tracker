# Using Protobuf with Python

## Installation

For Linux (Debian-based)

```bash
# Necessary dependencies
sudo apt-get install autoconf automake libtool curl make g++ unzip

# Taking source code
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git submodule update --init --recursive

# Compile C++ source code
./autogen.sh
./configure
make

# Install protobuf compiler in your system 
sudo make install
sudo ldconfig

# Checking if it works
protoc --version

# Compile protobuf for Python3
cd python
python setup.py build --cpp_implementation
python3 setup.py test

# Install Protobuf binding for your system
python3 setup.py install --cpp_implementation

```