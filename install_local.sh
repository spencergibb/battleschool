sudo pip uninstall -y battleschool
make sdist
VER=`cat lib/battleschool/__init__.py | grep version | awk '{ print $3}' | tr -d "'"`
sudo pip install dist/battleschool-${VER}.tar.gz
