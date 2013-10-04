

class CallbackModule(object):

    def display(self, event, *args):

        play = getattr(self, 'play', None)
        task = getattr(self, 'task', None)

        if play is not None:
            playbook = play.playbook.filename
        else:
            playbook = ""

        if task is not None:
            task_name = task.name
        else:
            task_name = ""

        print("%25s: play = %s, task = %s, args = %s" % (event, playbook, task_name, args))

    def on_any(self, *args, **kwargs):
        # play = getattr(self, 'play', None)
        # task = getattr(self, 'task', None)
        # print "on_any: play = %s, task = %s, args = %s, kwargs = %s" % (play, task, args, kwargs)
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        # self.display('runner_on_failed', host, res, ignore_errors)
        pass

    def runner_on_ok(self, host, res):
        # self.display('runner_on_ok', host, res)
        pass

    def runner_on_error(self, host, msg):
        # self.display('runner_on_error', host, msg)
        pass

    def runner_on_skipped(self, host, item=None):
        # self.display('runner_on_skipped', host, item)
        pass

    def runner_on_unreachable(self, host, res):
        # self.display('runner_on_unreachable', host, res)
        pass

    def runner_on_no_hosts(self):
        # self.display('runner_on_no_hosts')
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        self.display('runner_on_async_poll', host, res, jid, clock)

    def runner_on_async_ok(self, host, res, jid):
        self.display('runner_on_async_ok', host, res, jid)

    def runner_on_async_failed(self, host, res, jid):
        self.display('runner_on_async_failed', host, res, jid)

    def playbook_on_start(self):
        # self.display('playbook_on_start')
        pass

    def playbook_on_notify(self, host, handler):
        self.display('playbook_on_notify', host, handler)

    def playbook_on_no_hosts_matched(self):
        self.display('playbook_on_no_hosts_matched')

    def playbook_on_no_hosts_remaining(self):
        # self.display('playbook_on_no_hosts_remaining')
        pass

    def playbook_on_task_start(self, name, is_conditional):
        # self.display('playbook_on_task_start', name, is_conditional)
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        self.display('playbook_on_vars_prompt', varname, private, prompt, encrypt, confirm, salt_size, salt, default)

    def playbook_on_setup(self):
        # self.display('playbook_on_setup')
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        self.display('playbook_on_import_for_host', host, imported_file)

    def playbook_on_not_import_for_host(self, host, missing_file):
        self.display('playbook_on_not_import_for_host', host, missing_file)

    def playbook_on_play_start(self, pattern):
        # self.display('playbook_on_play_start', pattern)
        pass

    def playbook_on_stats(self, stats):
        # self.display('playbook_on_stats', stats)
        pass

