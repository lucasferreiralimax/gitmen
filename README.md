GitMan

GitMan is a command-line tool designed to streamline dependency management and Git repository status checks across multiple projects.

## Installation

### Prerequisites

- Python 3.x installed
- npm installed (for Node.js projects)
- Git installed

### Installation Steps

1. Clone the GitMan repository:
   ```bash
   git clone https://github.com/seu_usuario/gitman.git
   cd gitman
   ```

2. Install Python dependencies (if not installed):
   ```bash
   pip install .
   ```

3. Make the script executable (if needed):
   ```bash
   chmod +x gitman.py
   ```

4. Optionally, you can create a symbolic link to run `gitman` from anywhere:
   ```bash
   ln -s /path/to/gitman.py /usr/local/bin/gitman
   ```

## Usage

### Basic Commands

- Update dependencies in a specific project directory:
  ```bash
  gitman -u /path/to/project_directory
  ```

- Ignore specific dependencies during updates:
  ```bash
  gitman -u /path/to/project_directory -i dependency1,dependency2
  ```

- Check outdated dependencies across all projects:
  ```bash
  gitman -a
  ```

- Check Git status in all projects:
  ```bash
  gitman -g
  ```

- Update dependencies using `npm-check-updates` and commit changes:
  ```bash
  gitman -n /path/to/project_directory
  ```

### Additional Options

- Display program version:
  ```bash
  gitman -v
  ```

- Display help message:
  ```bash
  gitman --help
  ```
