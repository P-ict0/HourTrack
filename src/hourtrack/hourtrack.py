from .utils.argument_parser import parse_arguments
from .utils.config import DATA_FILE
from .utils.project_manager import ProjectManager
from .utils.logger import Logger
from .utils.project_manager import ProjectManager
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
        # Create a coloured logger
        self.logger = Logger(__name__).get_logger()

    def main(self):
        """
        Main function for the HourTrack application
        """
        # If the project name is not provided, use None
        project = getattr(self.args, "project", None)

        project_manager = ProjectManager(
            project, DATA_FILE, self.args.format, self.logger
        )

        if self.args.command == "start":
            project_manager.start_project()

        elif self.args.command == "stop":

            project_manager.stop_project()

        elif self.args.command == "list":
            if self.args.list_type == "all":
                project_manager.list_all_projects()
            elif self.args.list_type == "active":
                project_manager.list_active_projects()

        elif self.args.command == "status":
            output = getattr(self.args, "output", None)
            project_manager.project_status(output)

        elif self.args.command == "reset":
            handle_reset(args.project)

        elif self.args.command == "delete":
            handle_delete(args.project)

        elif self.args.command == "output":
            handle_output(args.project, args.format)


if __name__ == "__main__":
    main()
