import argparse

from importlib.metadata import version


def parse_arguments():
    """
    Parse command line arguments.

    Possible commands:
    - start <project>: Start tracking time for a project
    - stop <project>: Stop tracking time for a project
    - list all: List all projects (optionally with --format)
    - list active: List active projects (optionally with --format)
    - info [<project>]: Show status of a project or current session (optionally with --format and --output)
    - reset <project>: Reset timer for a project
    - edit <project>: Edit a project (rename, change session info, delete session, etc...)
    - delete <project>: Delete a project
    Options:
    - -f/--format: Output format for list, status, and output commands ("smart", "full", "short", "hours")
                    Default is "smart"
    - -o/--output: Output destination for status command
    - -a/--all: Apply to all projects
    - -g/--goal: Set an hour goal for a project
    - -h, --help: Show help message
    - -V, --version: Show version

    Returns: argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Track time spent on projects. It allows you to start, stop, edit and monitor time tracking for different projects, as well as output data to files.\n\
            For more information on a specific command, use `hourtrack <command> -h`\n\
                or refer to the manual at https://github.com/P-ict0/HourTrack."
    )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command")

    # Create command
    create_parser = subparsers.add_parser(
        "init", help="Create a new empty project but don't start tracking time"
    )
    create_parser.add_argument(
        "-g", "--goal", type=int, help="Set an hour goal for a project"
    )
    create_parser.add_argument("project", help="The name of the project to create")

    # Edit command
    edit_parser = subparsers.add_parser(
        "edit",
        help="Edit a project. You can rename a project or delete/add sessions",
    )
    edit_parser.add_argument("project", help="The name of the project to rename")
    edit_parser.add_argument(
        "--delete-session",
        type=int,
        help="Remove a session by its id (or `-1` for last session), which you can see using the `info` command",
        nargs="?",
    )
    edit_parser.add_argument(
        "--add-session",
        type=int,
        help="Add a session to a project ending now that started X hours ago.",
        nargs="?",
    )
    edit_parser.add_argument(
        "-g",
        "--goal",
        type=int,
        help="Add or edit a goal for a project in hours, or remove it by setting it to 0",
    )
    edit_parser.add_argument(
        "--rename", type=str, help="Rename a project with a new name", nargs="?"
    )

    # Start command, with a required project argument
    start_parser = subparsers.add_parser(
        "start",
        help="Start tracking time for a project, creating it if it doesn't exist",
    )
    start_parser.add_argument(
        "project", help="The name of the project to start tracking"
    )

    # Stop command, with a required project argument
    stop_parser = subparsers.add_parser(
        "stop", help="Stop tracking time for a project and finish the current session"
    )
    stop_parser.add_argument(
        "project", help="The name of the project to stop tracking", nargs="?"
    )
    stop_parser.add_argument(
        "-a", "--all", action="store_true", help="Stop all projects"
    )

    # List command, with a required list_type argument
    list_parser = subparsers.add_parser("list", help="List all or active projects")
    list_parser.add_argument(
        "list_type",
        choices=["all", "active"],
        help="List all, or active projects",
    )
    list_parser.add_argument(
        "-f",
        "--format",
        choices=["smart", "full", "short", "hours"],
        default="smart",
        help="Output format, default is 'smart'",
    )

    # Info command
    status_parser = subparsers.add_parser(
        "info",
        help="Show info of a project or of all projects, including time spent and sessions info, with option to output to a file",
    )
    status_parser.add_argument(
        "project",
        help="If provided, the name of the project to show status for",
        nargs="?",
    )
    status_parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output destination (file path)",
    )
    status_parser.add_argument(
        "-f",
        "--format",
        choices=["smart", "full", "short", "hours"],
        default="smart",
        help="Output format, default is 'smart'",
    )
    status_parser.add_argument(
        "-a", "--all", action="store_true", help="Show info for all projects"
    )

    # Reset command, with a required project argument
    reset_parser = subparsers.add_parser(
        "reset",
        help="Delete all sessions for a project or all projects and reset the timer to 0, but don't delete",
    )
    reset_parser.add_argument(
        "project", help="The name of the project to reset", nargs="?"
    )
    reset_parser.add_argument(
        "-a", "--all", action="store_true", help="Reset all projects"
    )

    # Delete command, with a required project argument
    delete_parser = subparsers.add_parser(
        "delete", help="Delete a project or all projects, removing all data"
    )
    delete_parser.add_argument(
        "project", help="The name of the project to delete", nargs="?"
    )
    delete_parser.add_argument(
        "-a", "--all", action="store_true", help="Delete all projects"
    )

    # Version command
    parser.add_argument(
        "-V", "--version", action="version", version=version("hourtrack")
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)  # Show the parsed arguments
