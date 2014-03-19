MODULE_PARAMS="pkg_type=app"
MODULE_PARAMS="$MODULE_PARAMS url=https://github.com/b4winckler/macvim/releases/download/snapshot-72/MacVim-snapshot-72-Mavericks.tbz"
MODULE_PARAMS="$MODULE_PARAMS archive_type=tar"
MODULE_PARAMS="$MODULE_PARAMS archive_path=MacVim-snapshot-72/MacVim.app"
MODULE_PARAMS="$MODULE_PARAMS creates=MacVim.app"

#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
