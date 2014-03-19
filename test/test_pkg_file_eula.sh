MODULE_PARAMS="pkg_name=org.TrueCryptFoundation.TrueCrypt"
MODULE_PARAMS="$MODULE_PARAMS pkg_version=7.1.1x"
MODULE_PARAMS="$MODULE_PARAMS archive_type=dmg"
MODULE_PARAMS="$MODULE_PARAMS src=/tmp/truecrypt.dmg"
MODULE_PARAMS="$MODULE_PARAMS archive_path='TrueCrypt 7.1a.mpkg'"
MODULE_PARAMS="$MODULE_PARAMS dmg_license=yes"
#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
