from abc import ABC
from abc import abstractmethod
from abc import abstractclassmethod
import argparse
from .modules import import_command_modules
import sys
from pathlib import Path


class BaseCommand(ABC):
    """
    All sub command classes must implement the setup_parser() and
    handle_commands() methods. The setup_parser() method is used to
    setup the parser for the command. It recieves the parent parser
    and should add a subparser to it and all the other subparsers
    and arguments to the subparser. The handle_commands() method
    is used to handle the command. It recieves the parsed arguments
    from the parser and act according to the recieved arguments.


    """

    @classmethod
    @abstractmethod
    def setup_parser(self, parser):
        """This is required to setup the parser for the command"""

    @classmethod
    @abstractmethod
    def create_parser(self, parser):
        """
        Create the parser for the command and register
        :param parser:
        :return:
        """

    @abstractmethod
    def handle_commands(self, args):
        """This is required to handle the command"""


class CommandImplementation(BaseCommand):
    command_name = None
    help = ""

    _methods = {}

    @classmethod
    def create_parser(cls, parser):
        cmd_parser = parser.add_parser(cls.command_name, help=cls.help)
        cls.setup_parser(cmd_parser)
        cls.parser = cmd_parser

    @classmethod
    def setup_parser(self, parser):
        raise NotImplementedError("setup_parser() not implemented")

    def handle_commands(self, args):
        raise NotImplementedError("handle_commands() not implemented")


class MainCommand:
    def __init__(
        self, main_command: str = None, version: str = None, description: str = None
    ):
        if main_command is None:
            main_command = Path(sys.argv[0]).stem

        self.main_command = main_command

        if description is None:
            description = f"Abakus Cloud {main_command} command line interface"

        self.description = description

        if version is None:
            version = "0.1"

        self.version = version

    def run(self):
        command_name = self.main_command
        description = self.description
        version = self.version
        import_command_modules()

        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s {version}".format(version=version),
        )

        parser.add_argument("--debug", action="store_true", help="Enable debug mode")

        subparsers: _SubParsersAction[ArgumentParser] | _SubParsersAction[
            Any
        ] = parser.add_subparsers(dest="command")

        # Get the command modules from the registry
        # that belongs to the upcloud_v1 command.

        from gl.cmdline.registry import registry

        command_klasses: dict[Any, Any] | Any = registry.get(command_name, {})

        for command_klass in command_klasses.values():
            """
            Any command_klass entry in the registry is a class that
            implements the BaseCommand abstract class or a subclass
            of CommandImplementation.

            The BaseCommand.setup_parser() method is a class method
            that is used to setup the parser for the command. This is
            where the subparser is added to the main parser.

            So here we use the "visitor pattern" to visit each of the
            setup_parser() methods of the command_klass entries in the
            registry.

            the subparsers object is passed by reference hence it is modified
            as it "visits" each of the command_klass entries.
            """
            command_klass.create_parser(subparsers)

        if len(command_klasses) == 0:
            print("No commands found for command: {}".format(command_name))
            sys.exit(1)

        args = parser.parse_args()

        if args.debug:
            print(args)
        cmd_klass = command_klasses.get(args.command, None)

        if cmd_klass is not None:
            cmd = cmd_klass()

            cmd.parser = parser
            cmd.handle_commands(args)
        else:
            parser.print_help()


def cmd_line():
    """
    This is the entry point for the command line interface.
    This is a generic entry point for the MainCommand class.

    To be able to have a custom command line interface for a command
    you need to subclass the MainCommand class. The subclass should
    be named after the command and should then a switch statement
    should be added to the code below to instantiate the correct
    command class and just default to the MainCommand class.

    TODO: Redesign this such that the MainCommand class is discovered
    using the Registry pattern. This way we can have a custom command
    line interface for each command without having to modify this file.

    :return:
    """
    path = Path(sys.argv[0])

    # get the filename from the path
    command_name = path.stem
    command = MainCommand(command_name, version="0.1")
    return command.run()
