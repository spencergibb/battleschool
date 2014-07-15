## battleschool

Development environment provisioning using [ansible](http://www.ansibleworks.com/docs/),
ala [boxen](http://boxen.github.com/) which uses [puppet](http://puppetlabs.com/puppet/what-is-puppet) and
[kitchenplan](https://github.com/kitchenplan/kitchenplan) which uses [chef](http://docs.opscode.com/)
Built on and for macs, but should be usable on Linux

See this [blog post](http://spencer.gibb.us/blog/2014/02/03/introducing-battleschool) for some background.

### install

    #if needed
    sudo easy_install pip

    sudo pip install battleschool

### install preview releases

    sudo pip install https://github.com/spencergibb/battleschool/releases/download/v0.x.0/battleschool-0.x.0.tar.gz

### running battleschool for the first time

    battle --config-file http://somesite/path/to/your/config.yml

As long as your `config.yml` doesn't have a `source.local` section (see [configuration](#configuration) below), you don't need to download or create a configuration for the first time.

### running battleschool

`battle`

### configuration

*NOTE: in the future, a default empty configuration will be created if you do not create one*

`mkdir ~/.battleschool`

put the following in `~/.battleschool/config.yml` and uncomment the items you want intstalled (remove the #)

    ---
    sources:
      local:
        #- playbook.yml

      url:
        #- name: playbook.yml
        #  url: https://db.tt/VcyI9dvr

      git:
        - name: 'osx'
          repo: 'https://github.com/spencergibb/ansible-osx'
          playbooks:
             #- adium.yml
             #- alfred.yml
             #- better-touch-tool.yml
             #- chrome-beta.yml
             #- dropbox.yml
             #- github.yml
             #- gitx.yml
             #- intellij-idea-ultimate.yml
             #- iterm2.yml
             #- java7.yml
             #- libreoffice.yml
             #- sequel-pro.yml
             #- skype.yml
             #- truecrypt.yml
             #- usb-overdrive.yml
             #- vagrant.yml
             #- virtualbox.yml
             #- xtra-finder.yml

[Here is my config.yml](https://db.tt/aG2uyydU)

[Here is my playbook.yml](https://db.tt/VcyI9dvr)

### explanation of ~/.battleschool/config.yml

#### local sources

    sources:
      local:
        - playbook.yml

Any [ansible playbooks](http://www.ansibleworks.com/docs/#playbooks) located in `~/.battleschool/playbooks`
can be listed under local.  Each playbook will be executed in order.  This can be useful for custom
configuration per workstation.  (You could install apps with homebrew or macports if those are installed, for example)

#### url sources

      url:
        - name: playbook.yml
          url: https://db.tt/VcyI9dvr

Playbooks located at a url.  Each playbook will be executed in order.  Helpful for bootstrapping (ie, the first time
you run battleschool.

#### git sources

    git:
      - name: 'osx'
        repo: 'https://github.com/spencergibb/ansible-osx'
        playbooks:
           - adium.yml

Any git repo that hosts ansible playbooks (specific to battleschool or not) will work here.  Each item under
playbooks is the relative location to a playbook in the specified git repository.  In the example above, `adium.yml`
is in the root of the ansible-osx repository.

#### git repo sources

Directory Layout

The top level of the directory would contain files and directories like so:

    local.yml                 # master playbook, after ansible-pull, automatically run, no need to list under playbooks
                              # NOT REQUIRED

    dev.yml                   # playbook for dev
    ux.yml                    # playbook for ux
    chrome.yml                # playbook for chrome

    roles/                    # standard ansible role hierarchy
    library/                  # remote module definitions

See the [roles docs](http://www.ansibleworks.com/docs/playbooks_roles.html) for information about ansible roles and
library is the location for placing [custom ansible modules](http://www.ansibleworks.com/docs/developing_modules.html)


#### the mac_pkg module

if you look most of the playbooks in [this git repo](https://github.com/spencergibb/ansible-osx) you will see the use of
the mac_pkg module.  Mac apps are usually a pkg (or mpgk) installer, or the bare .app directory.  They can be archived
in a number of formats: DMG or zip commonly.  Pkg files may not be archived at all.  Less common formats (tar or 7zip)
are not supported yet.

Lets look at adium.yml

    ---
    - hosts: workstation

      tasks:
        - name: install Adium
          mac_pkg: pkg_type=app
                   url=http://sourceforge.net/projects/adium/files/Adium_1.5.7.dmg/download
                   archive_type=dmg archive_path=Adium.app
          sudo: yes

`- hosts: workstation` this is required in each playbook as it targets the local workstation.  Though this is generally
arbitrary for most ansible users, it must be `workstation` in battleschool.

`pkg_type=app` type must be pkg or app.  Defaults to pkg

`url=....` the url of the app to download, alternatively `src=/local/path/to/app.dmg` may be used instead.

`archive_type=dmg` one of dmg, zip or none.  Defaults to none.

`archive_path=Adium.app` The path to the app or pkg in the archive.

`sudo: yes` required for mac_pkg tasks (this will prompt you to enter you sudo password only once)

*NOTE: battleschool, currently does not install apps from the Apple App Store.*


### common battle options

I alias battle to `battle -K`

    -K, --ask-sudo-pass   ask for sudo password

Force update of the playbooks from a VCS such as git

    -u, --update-vcs      update playbooks from a version control system (vcs)


### battle USAGE
    $ battle -h
    Usage: battle

    Options:
      -k, --ask-pass        ask for SSH password
      -K, --ask-sudo-pass   ask for sudo password
      -C, --check           don't make any changes; instead, try to predict some
                            of the changes that may occur
      --config-dir=CONFIG_DIR
                            config directory for battleschool
                            (default=/Users/spencergibb/.battleschool)
      --config-file=CONFIG_FILE
                            config file for battleschool
                            (default=/Users/spencergibb/.battleschool/config.yml)
      -c CONNECTION, --connection=CONNECTION
                            connection type to use (default=smart)
      -D, --diff            when changing (small) files and templates, show the
                            differences in those files; works great with --check
      -e EXTRA_VARS, --extra-vars=EXTRA_VARS
                            set additional key=value variables from the CLI
      -f FORKS, --forks=FORKS
                            specify number of parallel processes to use
                            (default=5)
      -h, --help            show this help message and exit
      -i INVENTORY, --inventory-file=INVENTORY
                            specify inventory host file
                            (default=/usr/share/battleschool/defaults/hosts)
      -l SUBSET, --limit=SUBSET
                            further limit selected hosts to an additional pattern
      --list-hosts          outputs a list of matching hosts; does not execute
                            anything else
      --list-tasks          do list all tasks that would be executed
      -M MODULE_PATH, --module-path=MODULE_PATH
                            specify path(s) to module library
                            (default=/usr/share/ansible/)
      -o, --one-line        condense output
      --private-key=PRIVATE_KEY_FILE
                            use this file to authenticate the connection
      --step                one-step-at-a-time: confirm each task before running
      -s, --sudo            run operations with sudo (nopasswd)
      --syntax-check        do a playbook syntax check on the playbook, do not
                            execute the playbook
      --tags=TAGS           only run plays and tasks tagged with these values
      -T TIMEOUT, --timeout=TIMEOUT
                            override the SSH timeout in seconds (default=10)
      -t TREE, --tree=TREE  log output to this directory
      -u, --update-source   update playbooks from sources(git, url, etc...)
      -v, --verbose         verbose mode (-vvv for more, -vvvv to enable
                            connection debugging)
      --version             show program's version number and exit

=================

TODO: cleanup cli output

TODO: more docs

TODO: default to ask sudo pass (simpler options).  Only don't ask if --no-sudo-pass is true
