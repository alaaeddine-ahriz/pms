import typer
import requests
from typing import Optional

app = typer.Typer(help="Project management commands.")

API_URL = "http://localhost:8000/api/v1"

@app.command()
def list(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """List projects with pagination."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/projects", headers=headers, params=params)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def create(nom: str = typer.Option(..., prompt=True), id_chef_chantier: Optional[int] = typer.Option(None), token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Create a new project."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"nom": nom}
    if id_chef_chantier:
        data["id_chef_chantier"] = id_chef_chantier
    response = requests.post(f"{API_URL}/projects", headers=headers, json=data)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def get(project_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Get a project by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/projects/{project_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}") 