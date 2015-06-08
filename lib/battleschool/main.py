import ansible.constants as AC
import battleschool.constants as C

# before callbacks import
AC.DEFAULT_CALLBACK_PLUGIN_PATH = C.DEFAULT_CALLBACK_PLUGIN_PATH

import ansible.playbook
import ansible.utils.template
from ansible import callbacks
from ansible import errors
from ansible import utils

from battleschool.__init__ import __version__
from battleschool.printing import *
from battleschool.source.git import Git
from battleschool.source.local import Local
from battleschool.source.url import Url

from copy import deepcopy
from tempfile import gettempdir
from sys import platform as _platform
from urlparse import urlparse

import json
import os
import platform
import sys
import tempfile

# TODO: verify environment: ansible

def getSourceHandlers():
    handlers = [Git, Local, Url]
    # TODO: auto load sources
    # for name, obj in inspect.getmembers(sourcepkg):
    #     if inspect.ismodule(obj):
    #         package = obj.__dict__['__package__']
    #         if package is not None and package.startswith('battleschool.source'):
    #             for srcName, srcObj in inspect.getmembers(obj):
    #                 if inspect.isclass(srcObj) and srcName != 'Source':
    #                     print "Loading %s/%s" % (srcName, srcObj)
    #                     handlers.append(srcObj)
    return handlers


def load_config_path(options, inventory, sshpass, sudopass):
    if options.config_file:
        config_file = options.config_file
        parse_result = urlparse(config_file)
        if parse_result.scheme:
            url_options = deepcopy(options)
            url_options.update_sources = True
            url_options.cache_dir = gettempdir()
            name = 'downloaded_config.yml'
            sources = {
                'url': [
                    {'name': name, 'url': config_file}
                ]
            }
            display(banner("Downloading config from url"))
            url = Url(url_options, sources)
            files = url.run(inventory, sshpass, sudopass)
            return files[0]
        else:
            return config_file

    return "%s/config.yml" % options.config_dir


def main(args, battleschool_dir=None):
    if not battleschool_dir:
        battleschool_dir = "%s/.battleschool" % os.environ['HOME']

    # TODO: make battle OO or more modular
    #-----------------------------------------------------------
    # make ansible defaults, battleschool defaults
    AC.DEFAULT_HOST_LIST = C.DEFAULT_HOST_LIST
    AC.DEFAULT_SUDO_FLAGS = C.DEFAULT_SUDO_FLAGS

    #-----------------------------------------------------------
    # create parser for CLI options
    usage = "%prog"
    parser = utils.base_parser(
        constants=AC,
        usage=usage,
        connect_opts=True,
        runas_opts=True,
        subset_opts=True,
        check_opts=True,
        diff_opts=True,
        output_opts=True
    )
    parser.version = "%s %s" % ("battleschool", __version__)
    # parser.add_option('--tags', dest='tags', default='all',
    #                   help="only run plays and tasks tagged with these values")
    parser.add_option('--syntax-check', dest='syntax', action='store_true',
                      help="do a playbook syntax check on the playbook, do not execute the playbook")
    parser.add_option('--list-tasks', dest='listtasks', action='store_true',
                      help="do list all tasks that would be executed")
    parser.add_option('--step', dest='step', action='store_true',
                      help="one-step-at-a-time: confirm each task before running")
    parser.add_option('--config-dir', dest='config_dir', default=None,
                      help="config directory for battleschool (default=%s)" % battleschool_dir)
    parser.add_option('--config-file', dest='config_file', default=None,
                      help="config file for battleschool (default=%s/%s)" % (battleschool_dir, "config.yml"))
    parser.add_option('-X', '--update-sources', dest='update_sources', default=False, action='store_true',
                      help="update playbooks from sources(git, url, etc...)")
    parser.add_option('--acquire-only', dest='acquire_only', default=False, action='store_true',
                      help="configure mac_pkg module to only aquire package (ie download only")

    options, args = parser.parse_args(args)
    # options.connection = 'local'

    playbooks_to_run = []  #[C.DEFAULT_PLAYBOOK]

    #-----------------------------------------------------------
    # setup inventory
    inventory = ansible.inventory.Inventory(options.inventory)
    inventory.subset(options.subset)
    if len(inventory.list_hosts()) == 0:
        raise errors.AnsibleError("provided hosts list is empty")

    #-----------------------------------------------------------
    # setup default options
    sshpass = None
    sudopass = None
    vault_pass = None
    options.remote_user = AC.DEFAULT_REMOTE_USER
    if not options.listhosts and not options.syntax and not options.listtasks:
        options.ask_pass = AC.DEFAULT_ASK_PASS
        options.ask_sudo_pass = options.ask_sudo_pass or AC.DEFAULT_ASK_SUDO_PASS
        passwds = utils.ask_passwords(ask_pass=options.ask_pass, become_ask_pass=options.ask_sudo_pass)
        sshpass = passwds[0]
        sudopass = passwds[1]
        vault_pass = passwds[2]
        # if options.sudo_user or options.ask_sudo_pass:
        #     options.sudo = True
        options.sudo_user = AC.DEFAULT_SUDO_USER

    extra_vars = utils.parse_extra_vars(options.extra_vars, vault_pass)
    only_tags = None  # options.tags.split(",")

    #-----------------------------------------------------------
    # setup config_dir and battleschool_dir
    if options.config_dir:
        battleschool_dir = options.config_dir
    else:
        options.config_dir = battleschool_dir

    #-----------------------------------------------------------
    # setup module_path
    if options.module_path is None:
        options.module_path = AC.DEFAULT_MODULE_PATH

    if options.module_path is None:
        options.module_path = C.DEFAULT_MODULE_PATH

    if C.DEFAULT_MODULE_PATH not in options.module_path:
        options.module_path = "%s:%s" % (C.DEFAULT_MODULE_PATH, options.module_path)

    #-----------------------------------------------------------
    # parse config data
    config_path = load_config_path(options, inventory, sshpass, sudopass)
    if os.path.exists(config_path) and os.path.isfile(config_path):
        config_data = utils.parse_yaml_from_file(config_path)
    else:
        config_data = {}

    #-----------------------------------------------------------
    # set config_dir
    if "cache_dir" in config_data:
        options.cache_dir = os.path.expanduser(config_data["cache_dir"])
    elif _platform == "darwin":  # OS X
        options.cache_dir = os.path.expanduser("~/Library/Caches/battleschool")
    else:
        options.cache_dir = "%s/cache" % battleschool_dir

    os.environ["BATTLESCHOOL_CACHE_DIR"] = options.cache_dir

    #-----------------------------------------------------------
    # setup extra_vars for later use
    if extra_vars is None:
        extra_vars = dict()

    extra_vars['battleschool_config_dir'] = battleschool_dir
    extra_vars['battleschool_cache_dir'] = options.cache_dir
    extra_vars['mac_pkg_acquire_only'] = options.acquire_only

    #-----------------------------------------------------------
    # set mac_version for extra_vars
    if _platform == "darwin":
        mac_version = platform.mac_ver()[0].split(".")
        extra_vars['mac_version'] = mac_version
        extra_vars['mac_major_minor_version'] = "%s.%s" % (mac_version[0], mac_version[1])

    #-----------------------------------------------------------
    # serialize extra_vars since there is now way to pass data
    # to a module without modifying every playbook
    tempdir = tempfile.gettempdir()
    extra_vars_path = os.path.join(tempdir, "battleschool_extra_vars.json")
    with open(extra_vars_path, 'w') as f:
        f.write(json.dumps(extra_vars))

    #-----------------------------------------------------------
    # setup and run source handlers
    handlers = getSourceHandlers()

    if 'sources' in config_data and config_data['sources']:
        sources = config_data['sources']
        display(banner("Updating sources"))
        for handler in handlers:
            source = handler(options, sources)
            playbooks = source.run(inventory, sshpass, sudopass)
            for playbook in playbooks:
                playbooks_to_run.append(playbook)
    else:
        display(banner("No sources to update"))

    #-----------------------------------------------------------
    # validate playbooks
    for playbook in playbooks_to_run:
        if not os.path.exists(playbook):
            raise errors.AnsibleError("the playbook: %s could not be found" % playbook)
        if not os.path.isfile(playbook):
            raise errors.AnsibleError("the playbook: %s does not appear to be a file" % playbook)

    become = True
    #-----------------------------------------------------------
    # run all playbooks specified from config
    for playbook in playbooks_to_run:
        stats = callbacks.AggregateStats()

        # let inventory know which playbooks are using so it can know the basedirs
        inventory.set_playbook_basedir(os.path.dirname(playbook))

        runner_cb = BattleschoolRunnerCallbacks()
        playbook_cb = BattleschoolCallbacks()
        #TODO: option to use default callbacks
        # runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        # playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)

        if options.step:
            playbook_cb.step = options.step

        pb = ansible.playbook.PlayBook(
            playbook=playbook,
            module_path=options.module_path,
            inventory=inventory,
            forks=options.forks,
            remote_user=options.remote_user,
            remote_pass=sshpass,
            callbacks=playbook_cb,
            runner_callbacks=runner_cb,
            stats=stats,
            timeout=options.timeout,
            transport=options.connection,
            become=become,
            become_method="sudo",
            become_user=options.sudo_user,
            become_pass=sudopass,
            extra_vars=extra_vars,
            private_key_file=options.private_key_file,
            only_tags=only_tags,
            check=options.check,
            diff=options.diff
        )

        if options.listhosts or options.listtasks:
            print ''
            print 'playbook: %s' % playbook
            print ''
            playnum = 0
            for (play_ds, play_basedir) in zip(pb.playbook, pb.play_basedirs):
                playnum += 1
                play = ansible.playbook.Play(pb, play_ds, play_basedir)
                label = play.name
                if options.listhosts:
                    hosts = pb.inventory.list_hosts(play.hosts)
                    print '  play #%d (%s): host count=%d' % (playnum, label, len(hosts))
                    for host in hosts:
                        print '    %s' % host
                if options.listtasks:
                    matched_tags, unmatched_tags = play.compare_tags(pb.only_tags)
                    unmatched_tags.discard('all')
                    unknown_tags = set(pb.only_tags) - (matched_tags | unmatched_tags)
                    if unknown_tags:
                        continue
                    print '  play #%d (%s): task count=%d' % (playnum, label, len(play.tasks()))
                    for task in play.tasks():
                        if set(task.tags).intersection(pb.only_tags):
                            if getattr(task, 'name', None) is not None:
                                # meta tasks have no names
                                print '    %s' % task.name
                print ''
            continue

        if options.syntax:
            # if we've not exited by now then we are fine.
            print 'Playbook Syntax is fine'
            return 0

        failed_hosts = []

        try:

            pb.run()

            hosts = sorted(pb.stats.processed.keys())
            # display(callbacks.banner("PLAY RECAP"))
            playbook_cb.on_stats(pb.stats)

            for host in hosts:
                smry = pb.stats.summarize(host)
                if smry['unreachable'] > 0 or smry['failures'] > 0:
                    failed_hosts.append(host)

            if len(failed_hosts) > 0:
                filename = pb.generate_retry_inventory(failed_hosts)
                if filename:
                    display("           to retry, use: --limit @%s\n" % filename)

            for host in hosts:
                smry = pb.stats.summarize(host)
                print_stats(host, smry)

            # print ""
            if len(failed_hosts) > 0:
                return 2

        except errors.AnsibleError, e:
            display("ERROR: %s" % e, color='red')
            return 1

    if not playbooks_to_run:
        display("\tWARNING: no playbooks run!", color='yellow')

    os.remove(extra_vars_path)
    display(banner("Battleschool completed"))
    # TODO: aggregate stats across playbook runs
