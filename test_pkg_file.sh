MODULE_PARAMS="name=com.oracle.jdk7u25"
MODULE_PARAMS="$MODULE_PARAMS state=present"
MODULE_PARAMS="$MODULE_PARAMS required_version=1.1"
MODULE_PARAMS="$MODULE_PARAMS src=/tmp/jdk7.dmg"
MODULE_PARAMS="$MODULE_PARAMS dmg_package='JDK 7 Update 25.pkg'"
#echo $MODULE_PARAMS
~/workspace/32degrees/ansible/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
