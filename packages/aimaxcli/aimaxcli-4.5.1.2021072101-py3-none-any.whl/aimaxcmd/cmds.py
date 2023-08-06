import abc
import six
from cliff.command import Command
import logging
import configparser
from aimaxsdk import errors


@six.add_metaclass(abc.ABCMeta)
class AIMaxCommand(Command):

    def get_parser(self, prog_name):
        parser = super(AIMaxCommand, self).get_parser(prog_name)
        if not self.app.interactive_mode:
            self._add_params(parser)
        else:
            self._add_params_interactive(parser)
        return parser

    def _add_params_interactive(self, parser):
        pass

    def _add_params(self, parser):
        parser.add_argument("--host", nargs=1, help="AIMax server address")
        parser.add_argument("--port", "-p", nargs=1, help="AIMax server port")
        parser.add_argument("--password", "-P", nargs=1, help="AIMax username")
        parser.add_argument("--username", "-u", nargs=1, help="AIMax password")
        parser.add_argument("--config-file", "-f", nargs=1, help="Config file "
                                                                 "containing AIMax authentication info")

    def take_action(self, parsed_args):
        self.log.debug(parsed_args)

    log = logging.getLogger(__name__)

    def _get_auth_info(self, parsed_args):
        auth_info = {}
        if parsed_args.config_file:
            config = configparser.ConfigParser()
            config.read(parsed_args.config_file[0], encoding="utf-8")
            auth_info["address"] = config.get("default", "address")
            auth_info["port"] = config.get("default", "port")
            auth_info["username"] = config.get("default", "username")
            auth_info["password"] = config.get("default", "password")
        else:
            if parsed_args.host is None:
                raise errors.ParamMissingException("AIMax server address is missing")
            auth_info["address"] = parsed_args.host[0]
            if parsed_args.port is None:
                raise errors.ParamMissingException("AIMax server port is missing")
            auth_info["port"] = parsed_args.port[0]
            if parsed_args.username is None:
                raise errors.ParamMissingException("AIMax username is missing")
            auth_info["username"] = parsed_args.username[0]
            if parsed_args.password is None:
                raise errors.ParamMissingException("AIMax password is missing")
            auth_info["password"] = parsed_args.password[0]
        return auth_info


class Connect(AIMaxCommand):

    def _add_params_interactive(self, parser):
        parser.add_argument("--host", nargs=1, help="AIMax server address")
        parser.add_argument("--port", "-p", nargs=1, help="AIMax server port")
        parser.add_argument("--password", "-P", nargs=1, help="AIMax username")
        parser.add_argument("--username", "-u", nargs=1, help="AIMax password")
        parser.add_argument("--config-file", "-f", nargs=1, help="Config file "
                                                                 "containing AIMax authentication info")

    def take_action(self, parsed_args):
        super(Connect, self).take_action(parsed_args)
        auth_info = self._get_auth_info(parsed_args)
        connections = self.app.connections
        connections.connect(auth_info["address"], auth_info["port"], auth_info["username"], auth_info["password"])
        self.log.info("Succeed to connect")
        self.app.auth_info = auth_info


class Disconnect(AIMaxCommand):

    def take_action(self, parsed_args):
        super(Disconnect, self).take_action(parsed_args)
        if self.app.interactive_mode:
            auth_info = self.app.auth_info
        else:
            auth_info = self._get_auth_info(parsed_args)
        connections = self.app.connections
        connections.disconnect(auth_info["address"], auth_info["port"], auth_info["username"])
        self.log.info("Succeed to disconnect")

    def _add_params(self, parser):
        parser.add_argument("--host", nargs=1, help="AIMax server address")
        parser.add_argument("--port", "-p", nargs=1, help="AIMax server port")
        parser.add_argument("--username", "-u", nargs=1, help="AIMax password")
        parser.add_argument("--config-file", "-f", nargs=1, help="Config file "
                                                                 "containing AIMax authentication info")

    def _get_auth_info(self, parsed_args):
        auth_info = {}
        if parsed_args.config_file:
            config = configparser.ConfigParser()
            config.read(parsed_args.config_file[0], encoding="utf-8")
            auth_info["address"] = config.get("default", "address")
            auth_info["port"] = config.get("default", "port")
            auth_info["username"] = config.get("default", "username")
        else:
            if parsed_args.host is None:
                raise errors.ParamMissingException("AIMax server address is missing")
            auth_info["address"] = parsed_args.host[0]
            if parsed_args.port is None:
                raise errors.ParamMissingException("AIMax server port is missing")
            auth_info["port"] = parsed_args.port[0]
            if parsed_args.username is None:
                raise errors.ParamMissingException("AIMax username is missing")
            auth_info["username"] = parsed_args.username[0]
        return auth_info
