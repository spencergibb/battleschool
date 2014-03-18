__author__ = 'spencergibb'


from . import Source


class Git(Source):
    """git source handler.
    """

    def type(self):
        return 'git'

    def dest_dir(self, source):
        dest_dir = "%s/%s" % (self.options.cache_dir, source['name'])
        return dest_dir

    def module_args(self, source):
        force = "no"
        update = "no"

        if self.options.update_sources:
            update = "yes"
            force = "yes"

        module_args = "repo=%s dest=%s force=%s update=%s " % \
                      (source['repo'], self.dest_dir(source), force, update)
        return module_args
