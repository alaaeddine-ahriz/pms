# PMS Efficience CLI

A command-line interface to interact with the PMS Efficience application via its API.

## Installation

1. Install dependencies (from the project root):

```bash
pip install -r requirements.txt
```

2. (Optional) Activate your virtual environment if you use one.

## Running the CLI

You can now run the CLI directly from the cli/ directory:

```bash
cd cli
chmod +x main.py  # (first time only)
./main.py [SUBCOMMANDS] [OPTIONS]
```

Or, from the project root:

```bash
python -m cli.main [SUBCOMMANDS] [OPTIONS]
```

## Available Subcommands

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

### Login and Save Token
```bash
python -m cli.main auth login
```

### List Projects
```bash
python -m cli.main projects list --token <YOUR_TOKEN>
```

### Create a New Employee
```bash
python -m cli.main hr create-employee --cin-numero 123456 --nom Doe --prenom John --etat-civil single --date-naissance 1990-01-01 --salaire-net 5000 --id-fonction 1 --token <YOUR_TOKEN>
```

### Upload a Document
```bash
python -m cli.main documents upload --file-path ./path/to/file.pdf --token <YOUR_TOKEN>
```

### Health Check
```bash
python -m cli.main common health
```

## Notes
- Most commands require a valid authentication token (`--token <YOUR_TOKEN>`), which you can obtain via the `auth login` command.
- Use `--help` with any subcommand to see available options, e.g.:

```bash
python -m cli.main projects --help
```

## Development
- Extend or add new subcommands in the `cli/` directory.
- The CLI uses [Typer](https://typer.tiangolo.com/) for command-line parsing and [requests](https://docs.python-requests.org/) for HTTP API calls. 