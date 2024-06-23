# GitMan

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

### Additional Commands

- Specify the base directory where projects are located (default is `~/Documents`):
  ```bash
  gitman -b /path/to/base_directory -u /path/to/project_directory
  ```

- Use a custom commit message when updating dependencies:
  ```bash
  gitman -u /path/to/project_directory -m "your custom commit message"
  ```

- Use a custom commit message with `npm-check-updates`:
  ```bash
  gitman -n /path/to/project_directory -m "your custom commit message"
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
