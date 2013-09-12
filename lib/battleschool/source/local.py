__author__ = 'spencergibb'


from . import Source


class Local(Source):
    """git source handler.
    """

    def type(self):
        return 'local'


    def run(self, inventory, sshpass, sudopass):
        playbooks = []

        if self.type() in self.sources:
            for source in self.sources[self.type()]:
                playbook = "%s/playbooks/%s" % (self.options.config_dir, source)
                playbooks.append(playbook)

        return playbooks


    def module_args(self, source):
        pass
