#!/usr/bin/env python3
import typer
import sys
from auth_cli import app as auth_app
from projects_cli import app as projects_app
from hr_cli import app as hr_app
from documents_cli import app as documents_app
from materials_cli import app as materials_app
from manufacturing_cli import app as manufacturing_app
from logistics_cli import app as logistics_app
from finance_cli import app as finance_app
from products_cli import app as products_app
from vehicles_cli import app as vehicles_app
from referentiels_cli import app as referentiels_app
from common_cli import app as common_app

app = typer.Typer(help="CLI for interacting with the PMS Efficience app.")

app.add_typer(auth_app, name="auth")
app.add_typer(projects_app, name="projects")
app.add_typer(hr_app, name="hr")
app.add_typer(documents_app, name="documents")
app.add_typer(materials_app, name="materials")
app.add_typer(manufacturing_app, name="manufacturing")
app.add_typer(logistics_app, name="logistics")
app.add_typer(finance_app, name="finance")
app.add_typer(products_app, name="products")
app.add_typer(vehicles_app, name="vehicles")
app.add_typer(referentiels_app, name="referentiels")
app.add_typer(common_app, name="common")

@app.command()
def interactive():
    """Launch interactive shell mode."""
    from interactive_shell import InteractiveCLI
    cli = InteractiveCLI()
    cli.run()

if __name__ == "__main__":
    # If no arguments provided, launch interactive mode
    if len(sys.argv) == 1:
        from interactive_shell import InteractiveCLI
        cli = InteractiveCLI()
        cli.run()
    else:
        app() 