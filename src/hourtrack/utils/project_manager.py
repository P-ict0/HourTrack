import json
import os
from datetime import datetime
from .helpers import ask_yes_no, format_time, format_timestamp
from typing import Optional
import sys


class ProjectManager:
    """
    Manage project tracking data, file format is JSON:

    Project not in active session:
    ```
    "projects": {
            "project1": {
                    "sessions": [
                        {"start": "2023-01-01 10:00:00", "end": "2023-01-01 12:00:00", total_time: 7200},
                        {"start": "2023-01-02 09:00:00", "end": "2023-01-02 11:00:00", total_time: 7200},
                    ]
            }
    }
    ```

    Project in active session:
    ```
    "projects": {
            "project1": {
                    "sessions": [
                        {"start": "2023-01-01 10:00:00", "end": "2023-01-01 12:00:00", total_time: 7200},
                        {"start": "2023-01-02 09:00:00", "end": "None", total_time: None},
                    ]
                }
            }
    ```
    """

    def __init__(
        self, project: Optional[str], data_file: str, format_mode: str
    ) -> None:
        """
        Initialize the ProjectManager

        :param project: The name of the project
        :param data_file: The path to the JSON file storing data
        :param format_mode: The mode to use for formatting time, one of "smart", "full", "short", "hours"
        """
        self.data_file = data_file  # path to the JSON file storing data
        self.project = project  # name of the project or None
        self.format_mode = format_mode
        self.init_file()  # initialize the JSON file
        self.data = self.load_data()  # pre-load the data from the JSON file

    def init_file(self) -> None:
        """
        Initialize the JSON file if it does not exist
        """

        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump({"projects": {}}, f)

    def load_data(self) -> dict:
        """
        Load data from the JSON file

        :return: The loaded data
        """
        with open(self.data_file, "r") as f:
            return json.load(f)

    def save_data(self, data: dict) -> None:
        """
        Save data to the JSON file

        :param data: The data to save
        """
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def exit_if_no_project(self) -> None:
        if not self.project:
            print("Project name is required")
            sys.exit(1)

    def start_project(self) -> None:
        """
        Start tracking the project, saving the start time
        """
        self.exit_if_no_project()
        if self.project not in self.data["projects"]:
            # If the project does not exist, create it
            if ask_yes_no(f"Project {self.project} does not exist. Create it?"):
                print(f"Creating project: {self.project}")
                self.data["projects"][self.project] = {"total_time": 0, "sessions": []}
        # Check if the project is already being tracked, to avoid starting a new session
        elif self.data["projects"][self.project]["sessions"] and self.data["projects"][self.project]["sessions"][-1]["end"] is None:
            print(f"Error: Project {self.project} is already being tracked")
            return

        # Add a new session with the start time
        self.data["projects"][self.project]["sessions"].append(
            {"start": datetime.now().isoformat(), "end": None, "total_time": None}
        )
        self.save_data(self.data)
        print(f"Started tracking project: {self.project}")

    def stop_project(self, apply_all: bool) -> None:
        """
        Stop tracking the project, saving the end time and calculating the total time
        Also saves the session data to the JSON file

        :param apply_all: Whether to stop tracking for all active projects
        """

        # Function to stop tracking a single project
        def stop_single_project(project: str) -> None:
            if project in self.data["projects"]:
                # Get the sessions for the project
                sessions = self.data["projects"][project]["sessions"]
                # Check if there is an active session
                if sessions and sessions[-1]["end"] is None:
                    # Update the end time for the session
                    sessions[-1]["end"] = datetime.now().isoformat()

                    # Calculate the total time for the session
                    start_time = datetime.fromisoformat(sessions[-1]["start"])
                    end_time = datetime.fromisoformat(sessions[-1]["end"])
                    session_total_time = int((end_time - start_time).total_seconds())
                    sessions[-1]["total_time"] = session_total_time

                    # Update the project's total time
                    self.data["projects"][project]["total_time"] += session_total_time

                    self.save_data(self.data)
                    print(f"Stopped tracking project: {project}")
                else:
                    # Only print if not applying to all projects
                    if not apply_all:
                        print(f"Project {project} is not currently being tracked")
            else:
                print(f"Error: Project {project} does not exist")

        # Stop tracking all projects
        if apply_all:
            ask_yes_no("Stop tracking all projects?")
            for project in list(
                self.data["projects"].keys()
            ):  # Use list to avoid runtime dictionary modification issues
                stop_single_project(project)
        else:
            self.exit_if_no_project()
            stop_single_project(self.project)

    def list_all_projects(self) -> None:
        """
        List all projects and their total times
        """
        # Iterate over the projects and print the total time
        for project, details in self.data["projects"].items():
            total_time = details["total_time"]
            # Check if the project is currently being tracked
            if details["sessions"] and details["sessions"][-1]["end"] is None:
                current_session_start = datetime.fromisoformat(
                    details["sessions"][-1]["start"]
                )
                current_session_time = int(
                    (datetime.now() - current_session_start).total_seconds()
                )
                total_time += current_session_time
                time_formatted = format_time(total_time, self.format_mode)
                print(f"  {project}: {time_formatted}  (active)")
                # Print the total time for the project
            else:
                time_formatted = format_time(total_time, self.format_mode)
                print(f"  {project}: {time_formatted}")

    def list_active_projects(self) -> None:
        """
        List all projects that are currently being tracked
        """
        # Iterate over the projects and print the total time
        for project, details in self.data["projects"].items():
            if details["sessions"] and details["sessions"][-1]["end"] is None:
                total_time = details["total_time"]
                current_session_start = datetime.fromisoformat(
                    details["sessions"][-1]["start"]
                )
                # Calculate the current session time
                current_session_time = int(
                    (datetime.now() - current_session_start).total_seconds()
                )
                total_time += current_session_time
                time_formatted = format_time(total_time, self.format_mode)
                print(f"  {project} (active): {time_formatted}")

    def create_project(self) -> None:
        """
        Create a new project
        """
        self.exit_if_no_project()
        if self.project in self.data["projects"]:
            print(f"Error: Project {self.project} already exists")
        else:
            self.data["projects"][self.project] = {"total_time": 0, "sessions": []}
            self.save_data(self.data)
            print(f"Created project: {self.project}")

    def rename_project(self, new_project: Optional[str]) -> None:
        """
        Rename a project

        :param new_project: The new name of the project
        """
        self.exit_if_no_project()
        if not new_project:
            new_project = input(f"New name for project '{self.project}': ")
        if self.project in self.data["projects"]:
            if new_project in self.data["projects"]:
                print(f"Error: Project {new_project} already exists")
            else:
                self.data["projects"][new_project] = self.data["projects"].pop(
                    self.project
                )
                self.save_data(self.data)
                print(f"Renamed project {self.project} to {new_project}")
        else:
            print(f"Error: Project {self.project} does not exist")

    def reset_project(self, apply_all: bool) -> None:
        """
        Reset the project, removing all session data and setting the total time to 0

        :param apply_all: Whether to reset all projects
        """

        # Function to reset a single project
        def reset_single_project(project: str) -> None:
            if project in self.data["projects"]:
                ask_confirmation = (
                    ask_yes_no(f"Reset project {project}?") if not apply_all else True
                )
                if ask_confirmation:
                    self.data["projects"][project] = {"total_time": 0, "sessions": []}
                    self.save_data(self.data)
                    print(f"Reset project {project}")
            else:
                print(f"Error: Project {project} does not exist")

        # Reset all projects
        if apply_all:
            ask_yes_no("Reset all projects?")
            for project in list(
                self.data["projects"].keys()
            ):  # Use list to avoid runtime dictionary modification issues
                reset_single_project(project)
        else:
            self.exit_if_no_project()
            reset_single_project(self.project)

    def delete_project(self, apply_all: bool) -> None:
        """
        Delete the project(s), removing all data.

        :param apply_all: Whether to delete all projects
        """

        def delete_single_project(project: str) -> None:
            if project in self.data["projects"]:
                ask_confirmation = (
                    ask_yes_no(f"Reset project {project}?") if not apply_all else True
                )
                if ask_confirmation:
                    del self.data["projects"][project]
                    self.save_data(self.data)
                    print(f"Deleted project {project}")
            else:
                print(f"Error: Project {project} does not exist")

        if apply_all:
            ask_yes_no("Delete all projects?")
            for project in list(
                self.data["projects"].keys()
            ):  # Use list to avoid runtime dictionary modification issues
                delete_single_project(project)
        else:
            self.exit_if_no_project()
            delete_single_project(self.project)

    def project_status(
        self, output_to_file: Optional[str] = None, apply_all: bool = False
    ) -> None:
        """
        Display the status of a project and optionally output it to a file

        :param apply_all: Whether to output the status of all projects
        :param output_to_file: Path to the file to output the status to
        """

        def output_project_status(project: str, details: dict) -> str:
            total_time = details["total_time"]
            num_sessions = len(details["sessions"])

            is_active = details["sessions"] and details["sessions"][-1]["end"] is None
            if is_active:
                current_session_start = datetime.fromisoformat(
                    details["sessions"][-1]["start"]
                )
                current_session_time = int(
                    (datetime.now() - current_session_start).total_seconds()
                )
                total_time += current_session_time
                active_warning = " (active)"
            else:
                active_warning = ""

            time_formatted = format_time(total_time, self.format_mode)

            status_output = f"Project name: {project}\n"
            status_output += f"Total time: {time_formatted}{active_warning}\n"
            status_output += f"Number of sessions: {num_sessions}\n\n"
            status_output += "Sessions:\n"
            for session in details["sessions"]:
                start = format_timestamp(session["start"])
                end = (
                    format_timestamp(session["end"])
                    if session["end"] is not None
                    else "Active"
                )
                session_total_time = (
                    format_time(session["total_time"], self.format_mode)
                    if session["total_time"]
                    else "N/A"
                )
                status_output += (
                    f"Start: {start}, End: {end}, Duration: {session_total_time}\n"
                )

            return status_output

        if apply_all:
            all_status_output = ""
            for project, details in self.data["projects"].items():
                all_status_output += output_project_status(project, details) + "\n"
                all_status_output += "-" * 40 + "\n"

            if output_to_file:
                with open(output_to_file, "w") as f:
                    f.write(all_status_output)
                print(f"Outputted status of all projects to {output_to_file}")
            else:
                print(all_status_output)
        else:
            if self.project:
                if self.project in self.data["projects"]:
                    project_status_output = output_project_status(
                        self.project, self.data["projects"][self.project]
                    )
                    if output_to_file:
                        with open(output_to_file, "w") as f:
                            f.write(project_status_output)
                        print(f"Outputted project {self.project} to {output_to_file}")
                    else:
                        print(project_status_output)
                else:
                    print(f"Error: Project '{self.project}' does not exist")
            else:
                # Check if there are any active projects
                active_projects = [
                    (proj, details)
                    for proj, details in self.data["projects"].items()
                    if details["sessions"] and details["sessions"][-1]["end"] is None
                ]

                if active_projects:
                    for proj, details in active_projects:
                        # Get the last session
                        last_session = details["sessions"][-1]
                        # Calculate the current session time
                        start_time = datetime.fromisoformat(last_session["start"])
                        current_time = datetime.now()
                        current_session_time = int(
                            (current_time - start_time).total_seconds()
                        )
                        current_session_time_formatted = format_time(
                            current_session_time, self.format_mode
                        )
                        print(f"Active project: {proj}")
                        print(
                            f"Current session total time: {current_session_time_formatted}"
                        )
                else:
                    print("There are no active projects")
