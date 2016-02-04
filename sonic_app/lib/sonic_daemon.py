from daemon import runner


class SonicDaemon:
    def __init__(self, app):
        self.app = app
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = self.app.pid
        self.pidfile_timeout = 5
        self.fh = self.app.fh

    def run(self):
        daemon_runner = runner.DaemonRunner(self.app)
        daemon_runner.daemon_context.files_preserve = [self.fh.stream]
        daemon_runner.daemon_context.initgroups = False
        daemon_runner.do_action()
