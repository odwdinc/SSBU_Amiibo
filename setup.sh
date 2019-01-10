#/bin/bash
cd "$PWD" & git submodule update --init --recursive
cd "$PWD/amiitool"
make
sudo make install PWD=$(pwd)