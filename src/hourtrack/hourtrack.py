import path
import sys

# directory reach
directory = path.Path(__file__)

# setting path
sys.path.append(directory.parent)

from utils.argument_parser import parse_arguments
from utils.config import DATA_FILE
from utils.project_manager import ProjectManager
from utils.project_manager import ProjectManager
import sys


class HourTrack:
    """
    Main class for the HourTrack application
    """

    def __init__(self) -> None:
        """
        Initialize the HourTrack application
        """

        # Parse command line arguments
        self.args = parse_arguments()
        self.check_args()

    def check_args(self):

        # If no command is provided, show the help message
        if not hasattr(self.args, "command"):
            print("Error: No command provided")
            sys.exit(1)

        if (
            self.args.command == "info"
            and hasattr(self.args, "output")
            and not hasattr(self.args, "project")
        ):
            print("Error: The --output argument requires the project argument\n")
            sys.exit(1)
        
        if self.args.command == "edit":
            if hasattr(self.args, "rename") and not hasattr(self.args, "project"):
                print("Error: The --rename argument requires the project argument\n")
                sys.exit(1)

    def track(self):
        """
        Main function for the HourTrack application
        """
        # If the project name is not provided, use None
        project = getattr(self.args, "project", None)
        format = getattr(self.args, "format", "smart")
        apply_all = getattr(self.args, "all", False)

        project_manager = ProjectManager(project, DATA_FILE, format)

        if self.args.command == "start":
            project_manager.start_project()

        elif self.args.command == "create":
            project_manager.create_project()

        elif self.args.command == "stop":
            project_manager.stop_project(apply_all)

        elif self.args.command == "reset":
            project_manager.reset_project(apply_all)

        elif self.args.command == "delete":
            project_manager.delete_project(apply_all)

        elif self.args.command == "edit":
            rename = getattr(self.args, "rename", None)
            add_session_hours = getattr(self.args, "add_session", None)
            remove_session_id = getattr(self.args, "delete_session", None)

            if rename:
                project_manager.rename_project(rename)
            elif add_session_hours:
                project_manager.add_session(add_session_hours)
            elif remove_session_id:
                project_manager.remove_session(remove_session_id)
            else:
                print("Error: No sufficient arguments provided for the edit command")
                sys.exit(1)

        elif self.args.command == "list":
            if self.args.list_type == "all":
                project_manager.list_all_projects()
            elif self.args.list_type == "active":
                project_manager.list_active_projects()

        elif self.args.command == "info":
            output = getattr(self.args, "output", None)
            project_manager.project_status(output, apply_all)


def run():
    hourtrack = HourTrack()
    hourtrack.track()
