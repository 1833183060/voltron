import logging

from voltron.view import *
from voltron.plugin import *
from voltron.api import *

log = logging.getLogger('view')

class CommandView (TerminalView):
    view_type = 'cmd'

    @classmethod
    def configure_subparser(cls, subparsers):
        sp = subparsers.add_parser('cmd', help='command view - specify a command to be run each time the debugger stops')
        VoltronView.add_generic_arguments(sp)
        sp.add_argument('command', action='store', help='command to run')
        sp.set_defaults(func=CommandView)

    def setup(self):
        self.config['cmd'] = self.args.command

    def render(self, error=None):
        # Set up header and error message if applicable
        self.title = '[cmd:' + self.config['cmd'] + ']'
        if error != None:
            self.body = self.colour(error, 'red')
        else:
            # Get the command output
            req = api_request('command')
            req.command = self.config['cmd']
            res = self.client.send_request(req)
            if res.is_success:
                # Get the command output
                self.body = res.output
            else:
                log.error("Error executing command: {}".format(res.message))
                self.body = self.colour(res.message, 'red')

        self.truncate_body()
        self.pad_body()

        # Call parent's render method
        super(CommandView, self).render()


class CommandViewPlugin(ViewPlugin):
    plugin_type = 'view'
    name = 'command'
    view_class = CommandView
