import json
import os
from datetime import datetime
from .helpers import ask_yes_no
from .helpers import format_time


class ProjectManager:
    """
    Manage project tracking data
    """

    def __init__(self, project: str, data_file: str, format_mode: str, logger) -> None:
        """
        Initialize the ProjectManager

        :param project: The name of the project
        :param data_file: The path to the JSON file storing data
        :param format_mode: The mode to use for formatting time, one of "smart", "full", "short", "hours"
        :param logger: The logger to use
        """
        self.data_file = data_file  # path to the JSON file storing data
        self.project = project  # name of the project
        self.format_mode = format_mode
        self.logger = logger
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

    def start_project(self) -> None:
        """
        Start tracking the project, saving the start time
        """
        if self.project not in self.data["projects"]:
            # If the project does not exist, create it
            if ask_yes_no(
                f"Project {self.project} does not exist. Create it? [Y]es/[n]o"
            ):
                self.data["projects"][self.project] = {"total_time": 0, "sessions": []}

        # Add a new session with the start time
        self.data["projects"][self.project]["sessions"].append(
            {"start": datetime.now().isoformat(), "end": None}
        )
        self.save_data(self.data)
        print(f"Started tracking project: {self.project}")

    def stop_project(self) -> None:
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
                self.data["projects"][self.project]["total_time"] += int(
                    (end_time - start_time).total_seconds()
                )
                self.save_data(self.data)
                self.logger.info(f"Stopped tracking project {self.project}")

            else:
                self.logger.info(
                    f"Project {self.project} is not currently being tracked"
                )
        else:
            self.logger.warning(f"Project {self.project} does not exist")

    def list_all_projects(self) -> None:
        """
        List all projects and their total times
        """
        print("Projects:")
        for project, details in self.data["projects"].items():
            total_time = details["total_time"]
            time_formatted = format_time(total_time, self.format_mode)
            print(f"  {project}: {time_formatted}")

    def list_active_projects(self) -> None:
        """
        List all projects that are currently being tracked
        """
        print("Active projects:")
        for project, details in self.data["projects"].items():
            if details["sessions"] and details["sessions"][-1]["end"] is None:
                total_time = details["total_time"]
                time_formatted = format_time(total_time, self.format_mode)
                print(f"  {project}: {time_formatted}")

    def reset_project(self) -> None:
        if self.project in self.data["projects"]:
            self.data["projects"][self.project] = {"total_time": 0, "sessions": []}
            self.save_data(self.data)
            self.logger.info(f"Reset project {self.project}")
        else:
            self.logger.warning(f"Project {self.project} does not exist")

    def delete_project(self, project: str) -> None:
        if project in self.data["projects"]:
            del self.data["projects"][project]
            self.save_data(self.data)
            print(f"Deleted project {project}")
        else:
            print(f"Project {project} does not exist")

    def output_raw_project(self, project: str) -> None:
        if project in self.data["projects"]:
            details = self.data["projects"][project]
            with open(f"{project}.csv", "w") as f:
                f.write("start,end\n")
                for session in details["sessions"]:
                    f.write(f"{session['start']},{session['end']}\n")
            print(f"Outputted project {project} to {project}.csv")
        else:
            print(f"Project '{project}' does not exist")
