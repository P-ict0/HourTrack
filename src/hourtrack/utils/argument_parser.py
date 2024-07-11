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
    - status [<project>]: Show status of a project or current session (optionally with --format and --output)
    - reset <project>: Reset timer for a project
    - delete <project>: Delete a project
    Options:
    - --format: Output format for list, status, and output commands ("smart", "full", "short", "hours")
                    Default is "smart"
    - --output: Output destination for status command
    - -h, --help: Show help message
    - -V, --version: Show version

    Returns: argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Track time spent on projects.")

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command")

    # Start command, with a required project argument
    start_parser = subparsers.add_parser(
        "start", help="Start tracking time for a project"
    )
    start_parser.add_argument(
        "project", help="The name of the project to start tracking"
    )

    # Stop command, with a required project argument
    stop_parser = subparsers.add_parser("stop", help="Stop tracking time for a project")
    stop_parser.add_argument("project", help="The name of the project to stop tracking")

    # List command, with a required list_type argument
    list_parser = subparsers.add_parser("list", help="List projects")
    list_parser.add_argument(
        "list_type",
        choices=["all", "active"],
        help="List all projects or only active ones",
    )
    list_parser.add_argument(
        "--format",
        choices=["smart", "full", "short", "hours"],
        default="smart",
        help="Output format",
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Show status of a project")
    status_parser.add_argument(
        "project",
        help="The name of the project to show status for",
        nargs="?",
    )
    status_parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output destination",
    )

    status_parser.add_argument(
        "--format",
        choices=["smart", "full", "short", "hours"],
        default="smart",
        help="Output format",
    )

    # Reset command, with a required project argument
    reset_parser = subparsers.add_parser("reset", help="Reset timer for a project")
    reset_parser.add_argument("project", help="The name of the project to reset")

    # Delete command, with a required project argument
    delete_parser = subparsers.add_parser("delete", help="Delete a project")
    delete_parser.add_argument("project", help="The name of the project to delete")

    # Version command
    parser.add_argument(
        "-V", "--version", action="version", version=version("hourtrack")
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)  # Show the parsed arguments
