# GitMen

GitMen is a command-line tool designed to streamline dependency management and Git repository status checks across multiple projects.

## Installation

### Prerequisites

- Python 3.x installed
- npm installed (for Node.js projects)
- Git installed

### Installation Steps

1. Clone the GitMen repository:
   ```bash
   git clone https://github.com/lucasferreiralimax/gitmen.git
   cd gitmen
   ```

2. Install Python dependencies (if not installed):
   ```bash
   pip install .
   ```

3. Make the script executable (if needed):
   ```bash
   chmod +x gitmen.py
   ```

4. Optionally, you can create a symbolic link to run `gitmen` from anywhere:
   ```bash
   ln -s /path/to/gitmen.py /usr/local/bin/gitmen
   ```

## Usage

### Basic Commands

- **Update dependencies in a specific project directory:**
  ```bash
  gitmen -u /path/to/project_directory
  ```

- **Ignore specific dependencies during updates:**
  ```bash
  gitmen -u /path/to/project_directory -i dependency1,dependency2
  ```

- **Check outdated dependencies across all projects:**
  ```bash
  gitmen -a
  ```

- **Check Git status in all projects:**
  ```bash
  gitmen -g
  ```

- **Update dependencies using `npm-check-updates` and commit changes:**
  ```bash
  gitmen -n /path/to/project_directory
  ```

### Additional Commands

- **Run a custom script on a project:**
  ```bash
  gitmen -s "custom script command"
  ```

- **Run an Angular-specific update process:**
  ```bash
  gitmen ng /path/to/project_directory
  ```

- **Fix Expo project dependencies:**
  ```bash
  gitmen expo /path/to/project_directory
  ```

- **Specify the base directory where projects are located (default is `~/Documents`):**
  ```bash
  gitmen -b /path/to/base_directory -u /path/to/project_directory
  ```

- **Use a custom commit message when updating dependencies:**
  ```bash
  gitmen -u /path/to/project_directory -m "your custom commit message"
  ```

- **Use a custom commit message with `npm-check-updates`:**
  ```bash
  gitmen -n /path/to/project_directory -m "your custom commit message"
  ```

### Repository and GitHub Integration

- **Check GitHub repositories linked to your account:**
  ```bash
  gitmen github
  ```

- **Clone repositories from GitHub by username:**
  ```bash
  gitmen clone username
  ```

### Language and Version

- **Select the language for the CLI interface:**
  ```bash
  gitmen language
  ```

- **Display program version:**
  ```bash
  gitmen -v
  ```

- **Display help message:**
  ```bash
  gitmen --help
  ```

## Learn More
### :performing_arts: Com quem você pode conversar sobre o projeto?
#### Who can you talk to about the project?
#### ¿Con quién puedes hablar sobre el proyecto?
#### С кем вы можете поговорить о проекте?
#### 誰がプロジェクトについて話すことができますか？
#### À qui pouvez-vous parler du projet?
#### Proje ile ilgili kiminle konuşabilirsin ?
#### 你能谈谈这个项目吗？

* :ghost: @lucasferreiralimax
* :email: lucasferreiralimax@gmail.com
