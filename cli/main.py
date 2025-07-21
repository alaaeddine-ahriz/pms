#!/usr/bin/env python3
import typer

app = typer.Typer(help="CLI for interacting with the PMS Efficience app.")

from .auth_cli import app as auth_app
app.add_typer(auth_app, name="auth")

from .projects_cli import app as projects_app
app.add_typer(projects_app, name="projects")

from .hr_cli import app as hr_app
app.add_typer(hr_app, name="hr")

from .documents_cli import app as documents_app
app.add_typer(documents_app, name="documents")

from .materials_cli import app as materials_app
app.add_typer(materials_app, name="materials")

from .manufacturing_cli import app as manufacturing_app
app.add_typer(manufacturing_app, name="manufacturing")

from .logistics_cli import app as logistics_app
app.add_typer(logistics_app, name="logistics")

from .finance_cli import app as finance_app
app.add_typer(finance_app, name="finance")

from .products_cli import app as products_app
app.add_typer(products_app, name="products")

from .vehicles_cli import app as vehicles_app
app.add_typer(vehicles_app, name="vehicles")

from .referentiels_cli import app as referentiels_app
app.add_typer(referentiels_app, name="referentiels")

from .common_cli import app as common_app
app.add_typer(common_app, name="common")

if __name__ == "__main__":
    app() 