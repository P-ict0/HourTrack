from .utils.argument_parser import parse_arguments
from .utils.config import DATA_FILE
from .utils.project_manager import ProjectManager
from .utils.logger import Logger


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

        if args.command == "start":
            handle_start(args.project)

        elif args.command == "stop":
            handle_stop(args.project)

        elif args.command == "list":
            if args.list_type == "all":
                handle_list_all(args.format)
            elif args.list_type == "active":
                handle_list_active(args.format)

        elif args.command == "status":
            handle_status(args.project, args.format)

        elif args.command == "reset":
            handle_reset(args.project)

        elif args.command == "delete":
            handle_delete(args.project)

        elif args.command == "output":
            handle_output(args.project, args.format)


if __name__ == "__main__":
    main()
