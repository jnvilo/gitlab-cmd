from gl.settings import settings
from importlib import import_module
import sys

registry = {}


def register_command(main_command):
    """
    This is used as a decorator to register a command class to the registry.
    The command class must have a command_name attribute which is the name
    of the command. The class name does not matter. The command_name attribute
    is used to register the command to the registry and is also used to fetch
    the class.

    :param main_command: The main command name. This is the name of the command
    :return: function
    """

    def inner(klass):
        if main_command not in registry:
            registry[main_command] = {}

        if klass.command_name is None:
            show_dev_help_for_commands(klass.__name__)
            sys.exit()
        registry[main_command][klass.command_name] = klass
        return klass

    return inner


def register_class_as_command(klass, main_command, command_name):
    ###
    # This is the old way of registering commands.
    # TODO: Remove this when all commands are registered with
    #       the decorator. Kept here for now for backwards compatibility.
    #       Will be removed when tests are updated and no more references
    #       to this function is found.
    ###
    if main_command not in registry:
        registry[main_command] = {command_name: klass}
    else:
        registry.update({command_name: klass})
    return registry

    registry[main_command][command_name] = klass
    return klass


def show_dev_help_for_commands(klass):
    """
    This is a helper function to show better error messages to developers
    using the cmdline module. This is not meant to be used in actual runtime.
    Only used when a developer forgets to add the command_name attribute or
    the command_name attribute is None during a runtime exception.
    :param klass:
    :return:
    """
    print("\nCommand class {} is missing command_name attribute".format(klass))
    print(
        """Example: 
            @register_command("upcloud_v1")
            class MyCommand(CommandImplementation):
                command_name = "restclient"
                help = "Upcloud restclient command subcommands" #Optional
    
           which will register the command to be invoked in a terminal as: 
           #> upcloud_v1 restclient 
           
    """
    )
