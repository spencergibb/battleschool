## battleschool
============

Development environment provisioning using ansible, ala boxen -> puppet, kitchenplan -> chef

### install

    sudo pip install https://github.com/32degrees/battleschool/releases/download/v0.1.0/battleschool-0.1.0.tar.gz


### remote source playbooks

Directory Layout

The top level of the directory would contain files and directories like so:

    local.yml                 # master playbook, after ansible-pull
    qa.yml                    # playbook for qa
    ux.yml                    # playbook for ux

    roles/                    # standard ansible role hierarchy
    library/                  # remote module definitions

TODO: Polish cli output

TODO: Docs

TODO: Submit pip

TODO: Submit mac port
