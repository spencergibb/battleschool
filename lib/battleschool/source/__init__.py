from battleschool.printing import BattleschoolRunnerCallbacks

__author__ = 'spencergibb'


import abc
import os
import sys

from ansible import errors
from ansible.callbacks import display
from ansible.runner import Runner


class Source(object):
    """Base class for source handlers.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, options, sources):
        self.options = options
        if (sources):
            self.sources = sources
        else:
            self.sources = {}
        return

    @abc.abstractmethod
    def type(self):
        pass

    @abc.abstractmethod
    def module_args(self, source):
        """Override to do something useful.
        """

    def has_source_type(self):
        return self.type() in self.sources and self.sources[self.type()] is not None

    def dest_dir(self, source):
        dest_dir = "%s/%s" % (self.options.cache_dir, source['name'])
        return dest_dir

    def module_name(self):
        return self.type()

    def add_playbook(self, playbooks, playbook):
        if os.path.exists(playbook) and os.path.isfile(playbook):
            playbooks.append(playbook)

    def run_module(self, inventory, source, sshpass, sudopass):
        runner_cb = BattleschoolRunnerCallbacks()
        runner_cb.options = self.options
        runner_cb.options.module_name = self.module_name()
        module_args = self.module_args(source)
        #TODO: get workstation from options
        runner = Runner(
            pattern='workstation',
            module_name=self.module_name(),
            module_path=self.options.module_path,
            module_args=module_args,
            inventory=inventory,
            callbacks=runner_cb,
            timeout=self.options.timeout,
            transport=self.options.connection,
            #sudo=self.options.sudo,
            become=False,
            become_method="sudo",
            become_user=self.options.sudo_user,
            become_pass=sudopass,
            check=self.options.check,
            diff=self.options.diff,
            private_key_file=self.options.private_key_file,
            remote_user=self.options.remote_user,
            remote_pass=sshpass,
            forks=self.options.forks
        )
        try:
            results = runner.run()
            for result in results['contacted'].values():
                if 'failed' in result or result.get('rc', 0) != 0:
                    display("ERROR: failed source type (%s) '%s': %s" % (self.type(), module_args, result['msg']),
                            stderr=True, color='red')
                    sys.exit(2)
            if results['dark']:
                display("ERROR: failed source type (%s) '%s': DARK" % (self.type(), module_args),
                        stderr=True, color='red')
                sys.exit(2)
        except errors.AnsibleError, e:
            # Generic handler for ansible specific errors
            display("ERROR: %s" % str(e), stderr=True, color='red')
            sys.exit(1)

    def run(self, inventory, sshpass, sudopass):
        playbooks = []
        if self.has_source_type():
            for source in self.sources[self.type()]:
                # print source
                self.run_module(inventory, source, sshpass, sudopass)

                source_playbooks = ["local.yml"]

                #add other playbooks relative to dest_dir from config.yml
                if "playbooks" in source and source['playbooks'] is not None:
                    for playbook in source['playbooks']:
                        # support for single level of directories in a playbook repo
                        if type(playbook) is dict:
                            for dir in playbook:
                                names = playbook[dir]
                                for name in names:
                                    playbook_name = "%s/%s" % (dir, name)
                                    if playbook_name not in source_playbooks:
                                        source_playbooks.append(playbook_name)
                        elif playbook not in source_playbooks:
                            source_playbooks.append(playbook)

                for playbook_name in source_playbooks:
                    suffix = ""

                    if not playbook_name.endswith(".yml") and not playbook_name.endswith(".yaml"):
                        suffix = ".yml"

                    playbook = "%s/%s%s" % (self.dest_dir(source), playbook_name, suffix)
                    self.add_playbook(playbooks, playbook)

        return playbooks
