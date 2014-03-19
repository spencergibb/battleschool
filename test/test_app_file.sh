MODULE_PARAMS="src=/tmp/Alfred.zip"
MODULE_PARAMS="$MODULE_PARAMS pkg_type=app"
MODULE_PARAMS="$MODULE_PARAMS archive_type=zip"
MODULE_PARAMS="$MODULE_PARAMS archive_path='Alfred 2.app'"
#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
