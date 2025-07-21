# PMS Efficience CLI

A command-line interface to interact with the PMS Efficience application via its API.

## Installation

1. Install dependencies (from the project root):

```bash
pip install -r requirements.txt
```

2. (Optional) Activate your virtual environment if you use one.

## Running the CLI

### Interactive Mode (Recommended)

Launch the interactive shell for seamless navigation:

```bash
cd cli
chmod +x main.py  # (first time only)
./main.py
```

This starts an interactive shell where you can:
- Navigate between modules without restarting
- Stay logged in across commands
- Get contextual help for each module

**Interactive Shell Usage:**
```
pms-cli> auth          # Enter auth module
pms-cli (auth)> login  # Login and save token
pms-cli (auth)> back   # Return to main menu
pms-cli> projects      # Enter projects module
pms-cli (projects)> list  # List projects (uses saved token)
pms-cli (projects)> help  # Show available commands
pms-cli (projects)> exit  # Exit the CLI
```

### Command Mode

You can also run individual commands directly:

```bash
cd cli
./main.py [SUBCOMMANDS] [OPTIONS]
```

Or, from the project root:

```bash
python -m cli.main [SUBCOMMANDS] [OPTIONS]
```

## Available Modules

- `auth` — Authentication (login, register, refresh)
- `projects` — Project management
- `hr` — Human resources (employees, tasks)
- `documents` — Document management
- `materials` — Materials management
- `manufacturing` — Manufacturing (BOM, orders)
- `logistics` — Logistics (deliveries, supply requests)
- `finance` — Finance (accounts, ledger, reports)
- `products` — Products, articles, stocks
- `vehicles` — Vehicles and drivers
- `referentiels` — Reference data (currencies, categories, statuses)
- `common` — Common utilities (health check)

## Example Usage

### Interactive Shell Workflow
```bash
./main.py                    # Start interactive mode
pms-cli> auth                # Enter auth module
pms-cli (auth)> login        # Login (saves token)
Email: user@example.com
Password: ********
Login successful. Token saved.

pms-cli (auth)> back         # Return to main menu
pms-cli> projects            # Enter projects module
pms-cli (projects)> list     # List projects (uses saved token automatically)
pms-cli (projects)> create   # Create new project
pms-cli (projects)> back     # Return to main menu
pms-cli> hr                  # Enter HR module
pms-cli (hr)> list-employees # List employees
pms-cli (hr)> quit           # Exit CLI
```

### Direct Commands
```bash
./main.py auth login
./main.py projects list
./main.py hr create-employee --cin-numero 123456 --nom Doe --prenom John
./main.py documents upload --file-path ./file.pdf
./main.py common health
```

## Authentication

The CLI automatically manages authentication tokens:
- Login once with `auth login` and the token is saved
- All subsequent commands use the saved token automatically
- Use `auth logout` to clear the token
- Token is stored in `~/.pms_cli_token`

## Navigation Commands

- `help` — Show help (context-aware)
- `modules` — List available modules
- `<module>` — Enter a module (e.g., `auth`, `projects`)
- `back` — Return to main menu (when in a module)
- `exit`/`quit` — Exit the CLI

## Notes

- The interactive shell shows your login status and current module
- Use `--help` with any command to see available options
- Most commands use the saved authentication token automatically
- For full command execution, some features may require using direct command mode

## Development

- Extend or add new modules in the `cli/` directory
- The CLI uses [Typer](https://typer.tiangolo.com/) for command-line parsing and [requests](https://docs.python-requests.org/) for HTTP API calls
- Interactive shell provides a user-friendly interface for exploring and using the API 