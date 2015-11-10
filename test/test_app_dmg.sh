MODULE_PARAMS="pkg_type=app"
MODULE_PARAMS="$MODULE_PARAMS archive_type=dmg"
MODULE_PARAMS="$MODULE_PARAMS archive_path=Adium.app"
MODULE_PARAMS="$MODULE_PARAMS url=http://sourceforge.net/projects/adium/files/Adium_1.5.10.dmg/download"
#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m lib/battleschool/share/library/mac_pkg -a "$MODULE_PARAMS"
