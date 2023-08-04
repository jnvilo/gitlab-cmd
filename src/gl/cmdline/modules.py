"""This module contains the functions that are used to import the command modules
and the functions that are used to get the list of command modules.
"""


from gl.settings import settings
from importlib import import_module


def get_all_command_files():
    """Get the list of files in the commands directory
    recursively and save them in a list and return it.

    The list is produced because we will need to import the files
    as modules. see: import_command_modules() function.

    How this works: We use the pathlib module to get the path to
    the commands directory. We then use the os.walk() function to
    get the list of files in the commands directory recursively.
    """

    from pathlib import Path
    import os

    # Get the path to the commands directory
    commands_dir = Path(Path(__file__).parent, "commands")

    # Get the path to the abakuscloud module
    module_dir = Path(__file__).parent.parent.parent

    files = []  # This will contain the list of module files

    # Walk the commands directory recursively and get the list of files
    # and then append them to the files list. We recursively walk the
    # directory because we want to get the list of files in the subdirectories
    # as well since the user of the application can create their own commands
    # and put them in the nested directories for better sorting and organization.

    for root, dirs, filenames in os.walk(commands_dir):
        for filename in filenames:
            if filename.endswith(".py") and filename != "__init__.py":
                path = Path(root, filename)
                filename = str(path.relative_to(module_dir))
                files.append(filename)
    return files


def get_command_modules():
    """Creates a list of the modules from the commands directory.
    We use the get_all_command_files() function to get the list of files
    and then we replace the '/' with '.' and remove the '.py' extension
    """

    files = get_all_command_files()
    modules = []
    for file in files:
        module = file.replace("/", ".").replace(".py", "")
        modules.append(module)
    return modules


def import_command_modules():
    """Import all the command modules from the commands directory."""

    modules = get_command_modules()
    for module in modules:
        import_module(module)
