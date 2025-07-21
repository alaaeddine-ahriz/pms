import typer
import requests
from typing import Optional
from auth_manager import get_auth_header

app = typer.Typer(help="Project management commands.")

API_URL = "http://localhost:8000/api/v1"

@app.command()
def list(page: int = 1, page_size: int = 10, token: Optional[str] = None):
    """List projects with pagination."""
    headers = get_auth_header(token)
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/projects", headers=headers, params=params)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def create(nom: str = typer.Option(..., prompt=True), id_chef_chantier: Optional[int] = typer.Option(None), token: Optional[str] = None):
    """Create a new project."""
    headers = get_auth_header(token)
    data = {"nom": nom}
    if id_chef_chantier:
        data["id_chef_chantier"] = id_chef_chantier
    response = requests.post(f"{API_URL}/projects", headers=headers, json=data)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def get(project_id: int, token: Optional[str] = None):
    """Get a project by ID."""
    headers = get_auth_header(token)
    response = requests.get(f"{API_URL}/projects/{project_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}") 