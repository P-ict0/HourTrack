<div align = center>
  
# ⌛ HourTrack

<br>

![Badge Workflow] 
[![Badge License]][License] 
![Badge Language] 
[![Badge Pull Requests]][Pull Requests] 
[![Badge Issues]][Issues] 

<br>

</div>

# Contents
- [📖 Description](#-description)
- [🚀 Quick start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [📲 Usage](#-usage)
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

# 🚀 Quick start

```bash
pipx install hourtrack
hourtrack start myProject
```

# ✨ Features

- **Supports multiple projects**: Track time for multiple projects.
- **Start/Stop tracking**: Start and stop tracking time for a project.
- **List projects**: List all projects being tracked.
- **Delete project**: Delete a project and all its data.
- **Reset project**: Reset a project's data.
- **Export data**: Export data to a `.txt` file.
- ...

# 📦 Installation

From [PyPI][PyPiLink]

```bash
pipx install hourtrack
```
_`pipx` is optional but recommended, you can use `pip` instead._

**Optional installation alternative**

```bash
git clone https://github.com/P-ict0/HourTrack.git
cd HourTrack
pipx install .  # You can also use `pip`
```

# 📲 Usage

For help:
```bash
hourtrack --help
```

**(Optional) Create a project**:
Create a project to start tracking time. (This is not necessary, as the project will be created when you start tracking time for it.)
```bash
hourtrack create <project>
```

**Start tracking**:
Start tracking session for a project. If the project does not exist, it will be created.
```bash
hourtrack start <project>
```

**Stop tracking**:
Stop current session for a project, saving the time spent. With option to delete all projects.
```bash
hourtrack stop <project|--all>
```

**Reset project**:
Reset a project's data. With option to reset all projects

```bash
hourtrack reset <project|--all>
```

**Rename project**:
Rename a project.
```bash
hourtrack rename <oldProject> [<newProject>]
```

**Delete project**:
Delete a project and all its data. With option to delete all projects.

```bash
hourtrack delete <project|--all>
```

**List projects**:
List all/active projects.

```bash
hourtrack list <all|active> [--format <smart|full|short|hours>]
```

**Project Info**:
Show the status of a specific project or show current active session. With option to output to a file.
```bash
# Project status
hourtrack info <project> [--format <smart|full|short|hours>] [-o <outputPath>]
# Active session
hourtrack info [--format <smart|full|short|hours>]
```

# ⚙ Options

| Command                 | Requirement                          | Default | Description                                                                                             |
|-------------------------|--------------------------------------|---------|---------------------------------------------------------------------------------------------------------|
| `hourtrack --help`      | None                                 | None    | For help                                                                                                |
| `hourtrack create <project>` | Project name                       | None    | Create a new empty project.                |
| `hourtrack start <project>` | Project name                       | None    | Start tracking session for a project. If the project does not exist, it will be created.                |
| `hourtrack stop <project\|--all>`  | Project name or `-a/--all` flag                       | None    | Stop current session for a project, saving the time spent. With option to stop all projects                                              |
| `hourtrack reset <project\|--all>` | Project name or `-a/--all` flag                       | None    | Reset a project's data. With option to reset all projects                                                                               |
| `hourtrack rename <oldProject> [<newProject>]` | Old project name                       | None    | Renames an already existing project                                                                               |
| `hourtrack delete <project\|--all>`| Project name or `-a/--all` flag                       | None    | Delete a project and all its data. With option to delete all projects                                                                     |
| `hourtrack list <all\|active> [--format <smart\|full\|short\|hours>]` | format `smart` | None | List all/active projects.                                                                               |
| `hourtrack info [<project>] [--format <smart\|full\|short\|hours>] [-o <outputPath>]` | format `smart` | None | Show the info of a specific project or show current active session if project is not specified. With option to output to a file.   |

# 💻 Development

```bash
git clone https://github.com/P-ict0/HourTrack.git
cd HourTrack
python -m venv venv
pip install -r requirements.txt
source venv/bin/activate # Windows: .\venv\Scripts\activate.ps1

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
