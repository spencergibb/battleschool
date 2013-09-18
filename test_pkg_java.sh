MODULE_PARAMS="name=com.oracle.jdk7u25"
MODULE_PARAMS="$MODULE_PARAMS state=present"
MODULE_PARAMS="$MODULE_PARAMS required_version=1.1"
MODULE_PARAMS="$MODULE_PARAMS dest=/tmp/jdk7.dmg"
MODULE_PARAMS="$MODULE_PARAMS cookie=gpw_e24=http%3A%2F%2Fwww.oracle.com"
#MODULE_PARAMS="$MODULE_PARAMS url=https://edelivery.oracle.com/otn-pub/java/jdk/7u25-b15/jdk-7u25-macosx-x64.dmg"
MODULE_PARAMS="$MODULE_PARAMS dmg_package='JDK 7 Update 25.pkg'"
#echo $MODULE_PARAMS
~/workspace/32degrees/ansible/hacking/test-module -m share/library/mac_pkg -a "$MODULE_PARAMS"
