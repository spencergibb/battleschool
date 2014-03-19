MODULE_PARAMS="pkg_name=com.vagrant.vagrant"
MODULE_PARAMS="$MODULE_PARAMS pkg_version=1.5.0"
MODULE_PARAMS="$MODULE_PARAMS archive_type=dmg"
MODULE_PARAMS="$MODULE_PARAMS archive_path=Vagrant.pkg"
#MODULE_PARAMS="$MODULE_PARAMS force=true"
MODULE_PARAMS="$MODULE_PARAMS url=https://dl.bintray.com/mitchellh/vagrant/vagrant_1.5.0.dmg"
#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
