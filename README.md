## battleschool
============

Development environment provisioning using ansible, ala boxen -> puppet, kitchenplan -> chef

### remote source playbooks

Directory Layout

The top level of the directory would contain files and directories like so:

    local.yml                 # master playbook, after ansible-pull
    qa.yml                    # playbook for qa
    ux.yml                    # playbook for ux

    roles/                    # standard ansible role hierarchy
    modules/                  # remote module definitions

TODO: Consolidated simple cli output

TODO: Docs

TODO: Submit mac port
