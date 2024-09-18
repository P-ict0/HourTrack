# ⌛ HourTrack

<br>

![Badge Workflow] 
[![Badge License]][License] 
![Badge Language] 
[![Badge Pull Requests]][Pull Requests] 
[![Badge Issues]][Issues] 

<br>

# Contents
- [📖 Description](#-description)
- [🚀 Quick start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [📲 Usage](#-usage)
  - [Help!](#help)
  - [Initialize a project](#initialize-a-project)
  - [Start tracking](#start-tracking)
  - [Stop tracking](#stop-tracking)
  - [Reset project](#reset-project)
  - [Edit project](#edit-project)
  - [Delete project](#delete-project)
  - [List projects](#list-projects)
  - [Project Info](#project-info)
- [⚙ Options](#-options)
- [💻 Development](#-development)
- [👥 Contributing](#-contributing)
<!----------------------------------------------------------------------------->

# 📖 Description

💻 **Windows, Linux and Mac compatible.** 💻

A Python script to track time spent on various projects. This script allows you to start, stop, and monitor time tracking for different projects, as well as output data to files.

It is very lightweight since it doesnt have to be running in the background.

This script is going to help you track:
- Total time spent on different projects
- Work sessions information
- Time spent on each session
- Set a goal for each project

# 🚀 Quick start

```bash
pip install hourtrack
hourtrack start myProject
```

_`pipx` is recommended, but you can use `pip` instead._

# ✨ Features

- **Supports multiple projects**: Track time for multiple projects.
- **Set goals**: Set an hour goal for each project.
- **Start/Stop tracking**: Start and stop tracking time for a project.
- **List projects**: List all projects being tracked.
- **Delete project**: Delete a project and all its data.
- **Reset project**: Reset a project's data.
- **Export data**: Export data to a `.txt` file.
- ...

# 📦 Installation

From [PyPI][PyPiLink]

```bash
pip install hourtrack
```

**Optional installation alternative**

```bash
git clone https://github.com/P-ict0/HourTrack.git
cd HourTrack
pip install .
```

# 📲 Usage

## Help!

```bash
hourtrack --help
hourtrack <command> --help
```

## Initialize a project

Create a project to start tracking time. You can also initialize a project with a goal.

```bash
hourtrack init <project>                  # Create a new empty project
hourtrack init <project> --goal <hours>   # Create a new project with a goal
```

## Start tracking

Start tracking session for a project. If the project does not exist, it will be created.
```bash
hourtrack start <project>
```

## Stop tracking

Stop current session for a project, saving the time spent. With option to delete all projects.
```bash
hourtrack stop <project> # Stop tracking for a project
hourtrack stop --all     # Stop tracking for all projects
```

## Reset project

Delete all sessions for a project or all projects and reset the timer to 0, but don't delete

```bash
hourtrack reset <project> # Reset a project
hourtrack reset --all     # Reset all projects
```

## Edit project

```bash
hourtrack edit <project> --rename <new_name>    # Rename a project

hourtrack edit <project> --goal <hours>         # Set/edit an hour goal for a project (or remove it with 0)

hourtrack edit <project> --add-session <hours>  # Add a session to a project 
                                                # ending now that started <hours> hours ago.

hourtrack edit <project> --delete-session <id>  # Delete session by its id (use `info` command to get the id)
hourtrack edit <project> --delete-session -1    # Delete last session
```

## Delete project

Delete a project and all its data. With option to delete all projects.

```bash
hourtrack delete <project> # Delete a project
hourtrack delete --all     # Delete all projects
```

## List projects

List all/active projects.

Available formats: `smart`, `full`, `short`, `hours`.
Note: If not specified, `smart` format is the default format.

```bash
hourtrack list all [-f <format>]      # List all projects
hourtrack list active [-f <format>]   # List active projects
```

## Project Info

Show the status of a specific project or of all projects. With option to output to a file.

Available formats: `smart`, `full`, `short`, `hours`.
Note: If not specified, `smart` format is the default format.
```bash
hourtrack info <project> [-f <format>]                      # Show project info
hourtrack info --all [-f <format>]                          # Show current active session info
hourtrack info <project|-all> -o <outputPath> [-f <format>] # Output to a file
```

# ⚙ Options

| Command                                                                                                           | Requirement                                                        | Default | Description                                                                                                                      |
|-------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------|
| `hourtrack --help`                                                                                                | None                                                               | None    | For help                                                                                                                         |
| `hourtrack init <project>`                                                                                        | Project name                                                       | None    | Create a new empty project.                                                                                                      |
| `hourtrack start <project>`                                                                                       | Project name                                                       | None    | Start tracking session for a project. If the project does not exist, it will be created.                                         |
| `hourtrack stop <project\|--all>`                                                                                 | Project name or `-a/--all` flag                                    | None    | Stop current session for a project, saving the time spent. With option to stop all projects                                      |
| `hourtrack reset <project\|--all>`                                                                                | Project name or `-a/--all` flag                                    | None    | Reset a project's data. With option to reset all projects                                                                        |
| `hourtrack edit <project> <--rename <name>\|--add-session <hours>\|--delete-session <id\|-1>\|-g/--goal <hours>>` | One of `--rename`, `--add-session`, `--delete-session`, `-g/--goal` | None    | Renames a project, edits hour goal, adds a session or deletes a session                                                          |
| `hourtrack delete <project\|--all>`                                                                               | Project name or `-a/--all` flag                                    | None    | Delete a project and all its data. With option to delete all projects                                                            |
| `hourtrack list <all\|active> [-f <smart\|full\|short\|hours>]`                                                   | None                                                               | format `smart` | List all/active projects.                                                                                                        |
| `hourtrack info [<project>] [-f <smart\|full\|short\|hours>] [-o <outputPath>]`                                   | None                                                               | format `smart` | Show the info of a specific project or show current active session if project is not specified. With option to output to a file. |

# 💻 Development

```bash
git clone https://github.com/P-ict0/HourTrack.git
cd HourTrack

# Note: You probably will need to remove the line from `utils/argument_parser.py`: from importlib.metadata import version
# And also remove the `version` option from the parser (below in the file).

# Run the script
python src/hourtrack.py --help
```

# 👥 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your suggested changes.

<!----------------------------------------------------------------------------->

[Stars]: https://starchart.cc/P-ict0/HourTrack
[DWS]: https://github.com/P-ict0/HourTrack

[Pull Requests]: https://github.com/P-ict0/HourTrack/pulls
[Issues]: https://github.com/P-ict0/HourTrack/issues
[PyPiLink]: https://pypi.org/project/hourtrack/

[License]: LICENSE

<!----------------------------------{ Badges }--------------------------------->

[Badge Workflow]: https://github.com/P-ict0/HourTrack/actions/workflows/release.yml/badge.svg

[Badge Issues]: https://img.shields.io/github/issues/P-ict0/HourTrack
[Badge Pull Requests]: https://img.shields.io/github/issues-pr/P-ict0/HourTrack
[Badge Language]: https://img.shields.io/github/languages/top/P-ict0/HourTrack
[Badge License]: https://img.shields.io/github/license/P-ict0/HourTrack
[Badge Lines]: https://img.shields.io/tokei/lines/github/P-ict0/HourTrack
