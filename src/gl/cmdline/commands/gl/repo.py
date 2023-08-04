from gl.cmdline.command import CommandImplementation
from gl.cmdline.registry import register_command


@register_command("gl")
class UpcloudServerCommand(CommandImplementation):
    command_name = "repo"
    help = "Work on repositories"

    @classmethod
    def setup_parser(self, parser):
        
        subparser = parser.add_subparsers(title="command",dest="command", required=True)

        create_parser = subparser.add_parser("create", help="Create a new repo")

        clone_parser = subparser.add_parser("clone", help="Clone a repo")           

        self.parser = parser

    def handle_commands(self, args):
        if args.command == "create":
            print("Creating repo")
        else:
            print(parser.print_help())