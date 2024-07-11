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

        # Add a new session with the start time
        self.data["projects"][self.project]["sessions"].append(
            {"start": datetime.now().isoformat(), "end": None, "total_time": None}
        )
        self.save_data(self.data)
        print(f"Started tracking project: {self.project}")

    def stop_project(self) -> None:
        self.exit_if_no_project()
        """
        Stop tracking the project, saving the end time and calculating the total time
        Also saves the session data to the JSON file
        """
        # Check if the project exists
        if self.project in self.data["projects"]:
            # Get the sessions for the project
            sessions = self.data["projects"][self.project]["sessions"]
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
                self.data["projects"][self.project]["total_time"] += session_total_time

                self.save_data(self.data)
                print(f"Stopped tracking project: {self.project}")
            else:
                print(f"Project {self.project} is not currently being tracked")
        else:
            print(f"Project {self.project} does not exist")

    def list_all_projects(self) -> None:
        """
        List all projects and their total times
        """
        print("Projects:")
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
                print(f"  {project} (active): {time_formatted}")
                # Print the total time for the project
            else:
                time_formatted = format_time(total_time, self.format_mode)
                print(f"  {project}: {time_formatted}")

    def list_active_projects(self) -> None:
        """
        List all projects that are currently being tracked
        """
        print("Active projects:")
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

    def reset_project(self) -> None:
        self.exit_if_no_project()
        if self.project in self.data["projects"]:
            if ask_yes_no(f"Reset project {self.project}?"):
                self.data["projects"][self.project] = {"total_time": 0, "sessions": []}
                self.save_data(self.data)
                print(f"Reset project {self.project}")
        else:
            print(f"Project {self.project} does not exist")

    def delete_project(self, project: str) -> None:
        self.exit_if_no_project()
        if project in self.data["projects"]:
            if ask_yes_no(f"Delete project {project}?"):
                del self.data["projects"][project]
                self.save_data(self.data)
            print(f"Deleted project {project}")
        else:
            print(f"Project {project} does not exist")

    def project_status(self, output_to_file: Optional[str] = None) -> None:
        """
        Display the status of a project and optionally output it to a file

        :param project: The name of the project
        :param output_to_file: Path to the file to output the status to
        """
        # Check if a project was provided, if not, output status of current active session, if any
        if self.project:
            # Check if the project exists
            if self.project in self.data["projects"]:
                details = self.data["projects"][self.project]
                total_time = details["total_time"]
                num_sessions = len(details["sessions"])

                is_active = (
                    details["sessions"] and details["sessions"][-1]["end"] is None
                )
                if is_active:
                    current_session_start = datetime.fromisoformat(
                        details["sessions"][-1]["start"]
                    )
                    current_session_time = int(
                        (datetime.now() - current_session_start).total_seconds()
                    )
                    total_time += current_session_time
                    active_warning = (
                        " (project is ACTIVE --> current session counted in total time)"
                    )
                else:
                    active_warning = ""

                time_formatted = format_time(total_time, self.format_mode)

                # Output the status to a file or to the console
                if output_to_file:
                    with open(f"{self.project}.txt", "w") as f:
                        f.write(f"Project name: {self.project}\n")
                        f.write(f"Total time: {time_formatted}{active_warning}\n")
                        f.write(f"Number of sessions: {num_sessions}\n\n")
                        f.write("Sessions:\n")
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
                            f.write(
                                f"Start: {start}, End: {end}, Duration: {session_total_time}\n"
                            )
                    print(f"Outputted project {self.project} to {self.project}.txt")
                else:
                    print(f"Status of project '{self.project}':")
                    print(f"Total time: {time_formatted}{active_warning}")
                    print(f"Number of sessions: {num_sessions}")
                    print("\nSessions:")
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
                        print(
                            f"Start: {start}, End: {end}, Duration: {session_total_time}"
                        )
            else:
                print(f"Project '{self.project}' does not exist")
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
