# This is a script for getting and installing VCFtools
cd 

git clone https://github.com/vcftools/vcftools.git

# need autoconf for the build
sudo apt install autoconf

# now to install VCFtools
cd vcftools/
./autogen.sh
./configure
make
make install


