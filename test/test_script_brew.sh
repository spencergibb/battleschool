MODULE_PARAMS="pkg_type=script"
MODULE_PARAMS="$MODULE_PARAMS script_creates=/usr/local/bin/brew"
#MODULE_PARAMS="$MODULE_PARAMS script_prefix='yes | '"
MODULE_PARAMS="$MODULE_PARAMS script_exe=/usr/bin/ruby"
MODULE_PARAMS="$MODULE_PARAMS url=https://raw.githubusercontent.com/Homebrew/install/master/install"
#MODULE_PARAMS="$MODULE_PARAMS script_postfix=' < /dev/null'"
MODULE_PARAMS="$MODULE_PARAMS script_data='\n'"
#echo $MODULE_PARAMS
$ANSIBLE_SRC_PATH/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
