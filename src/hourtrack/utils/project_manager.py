import json
import os
from datetime import datetime, timedelta
from .helpers import ask_yes_no, format_time, format_timestamp, write_to_file
from typing import Optional
import sys


class ProjectManager:
    """
    Manage project tracking data, file format is JSON:

    Project not in active session:
    ```
    "projects": {
            "project1": {
                    "hours_goal": 10,
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
                    "hours_goal": 10,
                    "sessions": [
                        {"start": "2023-01-01 10:00:00", "end": "2023-01-01 12:00:00", total_time: 7200},
                        {"start": "2023-01-02 09:00:00", "end": "None", total_time: None},
                    ]
                }
            }
    ```

    Project with hour goal:
    ```
    "projects": {
            "project1": {
                    "hours_goal": 10,
                    "sessions": [
                        {"start": "2023-01-01 10:00:00", "end": "2023-01-01 12:00:00", total_time: 7200},
                        {"start": "2023-01-02 09:00:00", "end": "2023-01-02 11:00:00", total_time: 7200},
                    ]
            }
    }
    ```

    Project with no hour goal:
    ```
    "projects": {
            "project1": {
                    "hours_goal": None,
                    "sessions": [
                        {"start": "2023-01-01 10:00:00", "end": "2023-01-01 12:00:00", total_time: 7200},
                        {"start": "2023-01-02 09:00:00", "end": "2023-01-02 11:00:00", total_time: 7200},
                    ]
            }
    }
    ```
    """

    def __init__(
        self,
        project: Optional[str],
        data_file: str,
        format_mode: str,
        hours_goal: Optional[int],
    ) -> None:
        """
        Initialize the ProjectManager

        :param project: The name of the project
        :param data_file: The path to the JSON file storing data
        :param format_mode: The mode to use for formatting time, one of "smart", "full", "short", "hours"
        :param hours_goal: The goal (hours) for the project
        """

        self.data_file = data_file  # path to the JSON file storing data
        self.project = project  # name of the project or None
        self.format_mode = format_mode  # mode to use for formatting time
        self.hours_goal = hours_goal  # goal (hours) for the project
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
            print("Error: Project name is required")
            sys.exit(1)

    def create_project(self) -> None:
        """
        Create a new project
        """
        self.exit_if_no_project()
        if self.project in self.data["projects"]:
            print(f"Error: Project {self.project} already exists")
        else:
            self.data["projects"][self.project] = {
                "hours_goal": self.hours_goal,
                "sessions": [],
            }
            self.save_data(self.data)
            print(f"Created project: {self.project}")

    def start_project(self) -> None:
        """
        Start tracking the project, saving the start time
        """
        self.exit_if_no_project()
        if self.project not in self.data["projects"]:
            # If the project does not exist, create it
            if ask_yes_no(f"Project {self.project} does not exist. Create it?"):
                print(f"Creating project: {self.project}")
                self.data["projects"][self.project] = {"hours_goal": 0, "sessions": []}
        # Check if the project is already being tracked, to avoid starting a new session
        elif (
            self.data["projects"][self.project]["sessions"]
            and self.data["projects"][self.project]["sessions"][-1]["end"] is None
        ):
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
            if ask_yes_no("Stop tracking all projects?"):
                for project in list(
                    self.data["projects"].keys()
                ):  # Use list to avoid runtime dictionary modification issues
                    stop_single_project(project)
        else:
            self.exit_if_no_project()
            stop_single_project(self.project)

    def add_session(self, hours: int) -> None:
        """
        Add a session to the project, with a specified number of hours

        :param hours: The number of hours to add to the session
        """
        self.exit_if_no_project()
        if self.project in self.data["projects"]:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)

            # Add a new session with the start and end time
            self.data["projects"][self.project]["sessions"].append(
                {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "total_time": hours * 3600,
                }
            )

            self.save_data(self.data)
            print(f"Added session to project: {self.project}")
        else:
            print(f"Error: Project {self.project} does not exist")

    def remove_session(self, session_id: int) -> None:
        """
        Remove a session from the project by its ID

        :param session_id: The ID of the session to remove
        """
        # User input is 1-indexed, convert to 0-indexed
        zero_indexed_id = session_id - 1

        # If user input is -1, remove the last session
        if session_id == -1:
            zero_indexed_id = -1

        self.exit_if_no_project()
        if self.project in self.data["projects"]:
            sessions = self.data["projects"][self.project]["sessions"]
            # Check if the session exists
            if len(sessions) > zero_indexed_id >= 0:
                confirm = ask_yes_no(
                    f"Remove session {session_id} from project {self.project}?"
                )
            # If the user wants to remove the last session
            elif zero_indexed_id == -1:
                confirm = ask_yes_no(
                    f"Remove the last session from project {self.project}?"
                )
            else:
                print(
                    f"Error: Session {session_id} does not exist for project {self.project}, see 'info' command for session IDs"
                )
                return

            if confirm:
                del sessions[zero_indexed_id]
                self.save_data(self.data)
                session_message = (
                    "session {session_id}" if session_id != -1 else "last session"
                )
                print(f"Removed {session_message} from project: {self.project}")
        else:
            print(f"Error: Project {self.project} does not exist")

    def set_goal(self, hours: int) -> None:
        """
        Set the goal for the project in hours

        :param hours: The goal for the project in hours
        """
        self.exit_if_no_project()
        if self.project in self.data["projects"]:
            if ask_yes_no(f"Edit goal for project {self.project} to {hours} hours?"):
                self.data["projects"][self.project]["hours_goal"] = hours
                self.save_data(self.data)
                print(f"Set goal for project {self.project} to {hours} hours")
        else:
            print(f"Error: Project {self.project} does not exist")

    def calculate_total_time(self, project: str) -> int:
        """
        Calculate the total time for the project

        :param project: The name of the project

        :return: The total time for the project
        """
        total_time = 0
        for session in self.data["projects"][project]["sessions"]:
            if session["end"]:
                total_time += session["total_time"]
            else:
                start_time = datetime.fromisoformat(session["start"])
                total_time += int((datetime.now() - start_time).total_seconds())
        return total_time

    def calculate_progress_string(self, project: str, only_values: bool = False) -> str:
        """
        Calculate the progress percentage and fraction for the project
        Example: 50.0% (5/10 hours)
        When more than 100% is reached, the percentage will remain 100
        Example: 100.0% (13/10 hours)
        When no goal is set, return an empty string

        :param project: The name of the project
        :param only_values: Whether to return only the values, without the '| Progress: ' prefix

        :return: The string representation of the progress percentage
        """
        if not self.has_goal(project):
            return ""

        total_time = self.calculate_total_time(project)
        hours_goal = self.data["projects"][project]["hours_goal"]
        progress_percentage = min((total_time / (hours_goal * 3600)) * 100, 100)
        progress_value = (
            f"{progress_percentage:.1f}% ({int(total_time / 3600)}/{hours_goal} hours)"
        )
        if only_values:
            return progress_value
        else:
            progress_string = f"| Progress: {progress_value}"
            return progress_string

    def is_project_active(self, project: str) -> bool:
        """
        Check if the project is currently being tracked

        :param project: The name of the project

        :return: Whether the project is active
        """
        if project in self.data["projects"]:
            project_data = self.data["projects"][project]
            sessions = project_data["sessions"]
            return sessions and sessions[-1]["end"] is None
        else:
            print(f"Error: Project {project} does not exist")

    def list_projects(self, active: bool = False) -> None:
        """
        List all projects and their total times, also display progress percentage if a goal is set
        """
        # Initialize counters for active and non-active projects
        active_projects = 0
        non_active_projects = 0
        output_non_active_projects = []
        output_active_projects = []

        # Loop through all projects
        for project in self.data["projects"].keys():
            total_time = self.calculate_total_time(project)
            progress = self.calculate_progress_string(project)
            time_formatted = format_time(total_time, self.format_mode)
            if self.is_project_active(project):
                active_projects += 1
                output_active_projects.append(
                    f"  {project}: {time_formatted} (active) {progress}"
                )
            else:
                non_active_projects += 1
                output_non_active_projects.append(
                    f"  {project}: {time_formatted} {progress}"
                )

        # Print the output
        if not active:
            print(
                f"Total projects: {active_projects + non_active_projects} (active: {active_projects}, non-active: {non_active_projects})"
            )
            for project in output_active_projects + output_non_active_projects:
                print(project)
        else:
            print(f"Number of active projects: {active_projects}")
            for project in output_active_projects:
                print(project)

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
                    self.data["projects"][project] = {"sessions": []}
                    self.save_data(self.data)
                    print(f"Reset project {project}")
            else:
                print(f"Error: Project {project} does not exist")

        # Reset all projects
        if apply_all:
            if ask_yes_no("Reset all projects?"):
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
                    ask_yes_no(f"Delete project {project}?") if not apply_all else True
                )
                if ask_confirmation:
                    del self.data["projects"][project]
                    self.save_data(self.data)
                    print(f"Deleted project {project}")
            else:
                print(f"Error: Project {project} does not exist")

        if apply_all:
            if ask_yes_no("Delete all projects?"):
                for project in list(
                    self.data["projects"].keys()
                ):  # Use list to avoid runtime dictionary modification issues
                    delete_single_project(project)
        else:
            self.exit_if_no_project()
            delete_single_project(self.project)

    def has_goal(self, project: str) -> bool:
        """
        Check if a project has a goal set

        :param project: The name of the project

        :return: Whether the project has a goal set
        """
        return self.data["projects"][project]["hours_goal"] != 0

    def project_status(
        self, output_to_file: Optional[str] = None, apply_all: bool = False
    ) -> None:
        """
        Display the status of a project and optionally output it to a file

        :param apply_all: Whether to output the status of all projects
        :param output_to_file: Path to the file to output the status to
        """

        def output_project_status(project: str) -> str:
            """
            Output the status of a single project

            :param project: The name of the project

            :return: The status output
            """
            total_time = self.calculate_total_time(project)
            num_sessions = len(self.data["projects"][project]["sessions"])
            progress = self.calculate_progress_string(project, only_values=True)

            is_active = self.is_project_active(project)
            if is_active:
                active_project_warning = " (active)"
            else:
                active_project_warning = ""

            time_formatted = format_time(total_time, self.format_mode)

            status_output = f"Project name: {project}\n"
            status_output += f"Total time: {time_formatted}{active_project_warning}\n"
            if self.has_goal(project):
                status_output += f"Progress: {progress}\n"
            if num_sessions == 0:
                status_output += "(Not Started)\n"
                return status_output
            status_output += f"Number of sessions: {num_sessions}\n\n"
            status_output += "Sessions:\n"
            for id, session in enumerate(self.data["projects"][project]["sessions"]):
                start = format_timestamp(session["start"])
                end = (
                    format_timestamp(session["end"])
                    if session["end"] is not None
                    else "Active"
                )
                session_total_time = (
                    # If the session is active, add active_session_warning and calculate the time until now, otherwise use the total_time
                    format_time(
                        (
                            int(
                                (
                                    datetime.now()
                                    - datetime.fromisoformat(session["start"])
                                ).total_seconds()
                            )
                            if session["end"] is None
                            else session["total_time"]
                        ),
                        self.format_mode,
                    )
                )
                status_output += f"Session {id+1}: Start: {start}, End: {end}, Duration: {session_total_time}\n"

            return status_output

        if apply_all:
            all_status_output = "-" * 40 + "\n"
            for project in list(
                self.data["projects"].keys()
            ):  # Use list to avoid runtime dictionary modification issues
                all_status_output += output_project_status(project) + "\n"
                all_status_output += "-" * 40 + "\n"

            if output_to_file:
                if not output_to_file.endswith(".txt"):
                    output_to_file += ".txt"
                if os.path.exists(os.path.dirname(output_to_file)):
                    if ask_yes_no(f"{output_to_file} already exists. Overwrite?"):
                        write_to_file(output_to_file, all_status_output)
                        print(f"Outputted status of all projects to {output_to_file}")
                    else:
                        sys.exit(0)

                write_to_file(output_to_file, all_status_output)
                print(f"Outputted status of all projects to {output_to_file}")
            else:
                print(all_status_output)
        else:
            if self.project:
                if self.project in self.data["projects"]:
                    project_status_output = output_project_status(self.project)
                    if output_to_file:
                        if not output_to_file.endswith(".txt"):
                            output_to_file += ".txt"
                        write_to_file(output_to_file, project_status_output)
                        print(f"Outputted project {self.project} to {output_to_file}")
                    else:
                        print(project_status_output)
                else:
                    print(f"Error: Project '{self.project}' does not exist")
