MODULE_PARAMS="pkg_name=org.macports.MacPorts"
MODULE_PARAMS="$MODULE_PARAMS pkg_version=0.2.2.0.0.0.0.0.0x"
#MODULE_PARAMS="$MODULE_PARAMS dest=/tmp/macports.pkg"
MODULE_PARAMS="$MODULE_PARAMS force=true"
MODULE_PARAMS="$MODULE_PARAMS url=https://distfiles.macports.org/MacPorts/MacPorts-2.2.0-10.8-MountainLion.pkg"
#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
