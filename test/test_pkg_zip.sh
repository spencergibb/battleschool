MODULE_PARAMS="pkg_name=org.macports.MacPorts"
MODULE_PARAMS="$MODULE_PARAMS pkg_version=1.0"
MODULE_PARAMS="$MODULE_PARAMS src=/tmp/macports.zip"
MODULE_PARAMS="$MODULE_PARAMS archive_type=zip"
MODULE_PARAMS="$MODULE_PARAMS archive_path=MacPorts-2.1.3-10.8-MountainLion.pkg"

#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
