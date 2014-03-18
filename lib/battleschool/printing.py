from ansible.callbacks import call_callback_module
from ansible.callbacks import display
from ansible.callbacks import DefaultRunnerCallbacks
from ansible.color import ANSIBLE_COLOR, stringc

import pprint

pp = pprint.PrettyPrinter()


def colorize(lead, num, color):
    """ Print 'lead' = 'num' in 'color' """
    if num != 0 and ANSIBLE_COLOR and color is not None:
        return "%s%s%s" % (stringc(lead, color), stringc("=", color), stringc(str(num), color))
    else:
        return "%s=%s" % (lead, str(num))


def hostcolor(host, stats, color=True):
    if ANSIBLE_COLOR and color:
        if stats['failures'] != 0 or stats['unreachable'] != 0:
            return "%s" % stringc(host, 'red')
        elif stats['changed'] != 0:
            return "%s" % stringc(host, 'yellow')
        else:
            return "%s" % stringc(host, 'green')
    return "%s" % host


def print_stats(host, smry):
    ok = smry['ok']
    changed = smry['changed']
    unreachable = smry['unreachable']
    failures = smry['failures']

    if unreachable > 0 or failures > 0:
        status = stringc("FAILED", "red")
    else:
        status = stringc("OK", "bright green")

    pattern = "\tPlaybook %s, %s, %s, %s, %s"

    display(pattern % (status,
        # hostcolor(host, smry, False),
        colorize('ok', ok, 'bright green'),
        colorize('changed', changed, 'yellow'),
        colorize('unreachable', unreachable, 'red'),
        colorize('failed', failures, 'red')),
            screen_only=True
    )

    display(pattern % (status,
        # hostcolor(host, smry, False),
        colorize('ok', ok, None),
        colorize('changed', changed, None),
        colorize('unreachable', unreachable, None),
        colorize('failed', failures, None)),
            log_only=True
    )


def banner(msg):
    #TODO: configurable size orig 78
    width = 110 - len(msg)
    if width < 3:
        width = 3
    filler = "#" * width
    return "## %s %s " % (msg, filler)


class BattleschoolRunnerCallbacks(DefaultRunnerCallbacks):
    """ callbacks for use by battles """

    def get_play(self):
        if self.runner:
            return self.runner
        if self.task:
            return self.task
        return self.play

    def get_name(self):
        if self.runner:
            return self.get_play().module_name
        return self.get_play().name

    def on_failed(self, host, res, ignore_errors=False):
        if not ignore_errors:
            display("\tTask FAILED: %s %s" % (self.get_name(), res['msg']), color="red")
        super(BattleschoolRunnerCallbacks, self).on_failed(host, res, ignore_errors=ignore_errors)

    def on_ok(self, host, res):
        if 'msg' in res:
            msg = ": %s" % res['msg']

            if 'item' in res:
                msg = "%s => item=%s" % (msg, res['item'])
        else:
            msg = ''

        try:
            if self.get_play():
                display("\tTask OK: %s%s" % (self.get_name(), msg))
        except AttributeError:
            invocation = res['invocation']
            msg = invocation['module_args']
            module_name = invocation['module_name']

            #TODO: move this?
            if module_name == 'git':
                args = dict()
                tokens = invocation['module_args'].split()
                for token in tokens:
                    pair = token.split("=")[:2]
                    args[pair[0]] = pair[1]
                msg = args['repo']

            display("\tTask OK: %s, changed=%s %s" % (module_name, res['changed'], msg))
        super(BattleschoolRunnerCallbacks, self).on_ok(host, res)

    def on_unreachable(self, host, results):
        item = None
        if type(results) == dict:
            item = results.get('item', None)
        if item:
            msg = "\tFailed Task: %s => (item=%s) => %s" % (host, item, results)
        else:
            msg = "\tFatal Task: %s => %s" % (host, results)
        display(msg, color='red', runner=self.runner)
        super(BattleschoolRunnerCallbacks, self).on_unreachable(host, results)

    def on_skipped(self, host, item=None):
        display("\tTask skipped: %s" % self.get_name(), color="yellow")
        super(BattleschoolRunnerCallbacks, self).on_skipped(host, item)

    def on_error(self, host, err):
        display("\tTask ERROR: %s%s" % (self.get_name(), err), color="red")
        super(BattleschoolRunnerCallbacks, self).on_error(host, err)

    def on_no_hosts(self):
        display("\tTask NO HOSTS: %s" % self.get_name(), color="red")
        super(BattleschoolRunnerCallbacks, self).on_no_hosts()

    def on_async_poll(self, host, res, jid, clock):
        super(BattleschoolRunnerCallbacks, self).on_async_poll(host, res, jid, clock)

    def on_async_ok(self, host, res, jid):
        super(BattleschoolRunnerCallbacks, self).on_async_ok(host, res, jid)

    def on_async_failed(self, host, res, jid):
        super(BattleschoolRunnerCallbacks, self).on_async_failed(host,res,jid)

    def on_file_diff(self, host, diff):
        super(BattleschoolRunnerCallbacks, self).on_file_diff(host, diff)


class BattleschoolCallbacks(object):
    """ used by battle for playbooks """

    def __init__(self, verbose=False):

        self.verbose = verbose

    def on_start(self):
        call_callback_module('playbook_on_start')

    def on_notify(self, host, handler):
        call_callback_module('playbook_on_notify', host, handler)

    def on_no_hosts_matched(self):
        call_callback_module('playbook_on_no_hosts_matched')

    def on_no_hosts_remaining(self):
        display("\tFailed playbook: %s" % self.playbook.filename, color='bright red')
        call_callback_module('playbook_on_no_hosts_remaining')

    def on_task_start(self, name, is_conditional):
        call_callback_module('playbook_on_task_start', name, is_conditional)

    def on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        call_callback_module( 'playbook_on_vars_prompt', varname, private=private, prompt=prompt,
                              encrypt=encrypt, confirm=confirm, salt_size=salt_size, salt=None, default=default )

    def on_setup(self):
        call_callback_module('playbook_on_setup')

    def on_import_for_host(self, host, imported_file):
        call_callback_module('playbook_on_import_for_host', host, imported_file)

    def on_not_import_for_host(self, host, missing_file):
        call_callback_module('playbook_on_not_import_for_host', host, missing_file)

    def on_play_start(self, pattern):
        display(banner("Executing playbook %s" % self.playbook.filename), color="bright blue")
        call_callback_module('playbook_on_play_start', pattern)

    def on_stats(self, stats):
        call_callback_module('playbook_on_stats', stats)
