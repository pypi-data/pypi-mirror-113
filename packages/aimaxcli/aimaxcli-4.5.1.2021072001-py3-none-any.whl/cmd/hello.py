from cliff.command import Command
import logging


class Hello(Command):

    def take_action(self, parsed_args):
        self.log.info("Hello")

    log = logging.getLogger(__name__)