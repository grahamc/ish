
import sys
import os
import random


class View:
    def __init__(self, caller, err=sys.stderr, out=sys.stdout, exit=sys.exit,
                 execvp=os.execvp):
        self.caller = caller
        self.err = err
        self.out = out
        self.exit = exit
        self.execvp = execvp

    def stderr(self, msg):
        self.err.write("{}\n".format(msg))

    def stdout(self, msg):
        self.out.write("{}\n".format(msg))

    def help(self):
        self.stderr("Usage: {} target [ssh parameters]".format(self.caller))
        self.exit(1)

    def valid_targets(self, targets):
        for key in sorted([key for key in targets]):
            self.stdout(key)

        self.exit(0)

    def invalid_target(self, attempted_target):
        self.stderr("No target named {}".format(attempted_target))
        self.exit(1)

    def connect_to(self, selected_ip, all_ips, target):
        self.stderr("Found {} IPs for {}:".format(len(all_ips), target))
        for ip in all_ips:
            if ip == selected_ip:
                self.stderr(" - {} (selected)".format(ip))
            else:
                self.stderr(" - {}".format(ip))

        cmd = '/usr/bin/ssh'
        arguments = [cmd, selected_ip]
        arguments.extend(sys.argv[2:])

        self.execvp(cmd, arguments)
        self.exit(2)


class InputHandler:
    def __init__(self, argv, targets, ui=View):
        self.argv = argv
        self.ui = ui(argv[0])
        self.targets = targets

    def handle_argv(self):
        if len(self.argv) == 1:
            self.ui.help()
        else:
            arg1 = self.argv[1]

            if arg1 == '--completion':
                self.ui.valid_targets(self.targets)
            elif arg1 in self.targets:
                ips = sorted(self.targets[arg1])
                selected_ip = random.choice(ips)
                self.ui.connect_to(selected_ip, ips, arg1)
            else:
                self.ui.invalid_target(arg1)
