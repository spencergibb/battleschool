__author__ = 'spencergibb'


from . import Source


class Url(Source):
    """url source handler.
    """

    def type(self):
        return 'url'

    def module_name(self):
        return 'get_url'

    def dest_dir(self, source):
        return self.options.cache_dir

    def module_args(self, source):
        force = "no"

        if self.options.update_sources:
            force = "yes"

        module_args = "url=%s dest=%s/%s force=%s validate_certs=no " % \
                      (source["url"], self.dest_dir(source), source["name"], force)

        if "playbooks" not in source:
            source["playbooks"] = []

        source["playbooks"].append(source["name"])
        return module_args
