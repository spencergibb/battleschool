This portfile installs battleschool from the git repository, it will install the
latest and greatest version of battleschool. This portfile does not install the
required dependancies to run in fireball mode.

## Installing the stable version of battleschool via macports

If you wish to run a stable version of battleschool please do the following

First update your macports repo to the latest versions

  $ sudo port sync

Then install battleschool

  $ sudo port install battleschool

## Installing the devel version of battleschool via macports

To use this Portfile to install the development version of battleschool one should
follow the instructions at
<http://guide.macports.org/#development.local-repositories>

The basic idea is to add the _battleschool/packaging/macports_ directory to your
_/opt/local/etc/macports/sources.conf_ file. You should have something similar
to this at the end of the file

  file:///Users/sgibb/develop/battleschool/packaging/macports
  rsync://rsync.macports.org/release/tarballs/ports.tar [default]

In the _battleschool/packaging/macports_ directory, do this

  $ portindex

Once the index is created the _Portfile_ will override the one in the upstream
macports repository.

Installing newer development versions should involve an uninstall, clean,
install process or else the Portfile will need its version number/epoch
bumped.
