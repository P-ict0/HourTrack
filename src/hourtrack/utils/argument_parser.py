import argparse


def parse_arguments():
    """
    Parse command line arguments.

    Possible commands:
    - start <project>: Start tracking time for a project
    - stop <project>: Stop tracking time for a project
    - list all: List all projects (optionally with --format)
    - list active: List active projects (optionally with --format)
    - status <project>: Show status of a project (optionally with --format)
    - reset <project>: Reset timer for a project
    - delete <project>: Delete a project
    - output <project>: Output project data to file (optionally with --format)

    Options:
    - --format: Output format for list, status, and output commands ("smart", "full", "short", "hours")
                    Default is "smart"



    Returns: argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Track time spent on projects.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Start command
    start_parser = subparsers.add_parser(
        "start", help="Start tracking time for a project"
    )
    start_parser.add_argument(
        "project", help="The name of the project to start tracking"
    )

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop tracking time for a project")
    stop_parser.add_argument("project", help="The name of the project to stop tracking")

    # List command
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
        "project", help="The name of the project to show status for"
    )
    status_parser.add_argument(
        "--format",
        choices=["smart", "full", "short", "hours"],
        default="smart",
        help="Output format",
    )

    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset timer for a project")
    reset_parser.add_argument("project", help="The name of the project to reset")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a project")
    delete_parser.add_argument("project", help="The name of the project to delete")

    # Output command
    output_parser = subparsers.add_parser("output", help="Output project data to file")
    output_parser.add_argument(
        "project", help="The name of the project to output data for"
    )
    output_parser.add_argument(
        "--format",
        choices=["smart", "full", "short", "hours"],
        default="smart",
        help="Output format",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)  # For testing purposes, to see the parsed arguments
