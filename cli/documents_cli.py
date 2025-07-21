import typer
import requests
from typing import Optional

app = typer.Typer(help="Document management commands.")

API_URL = "http://localhost:8000/api/v1/documents"

@app.command()
def upload(file_path: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Upload a document."""
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(f"{API_URL}/", headers=headers, files=files)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def get_metadata(document_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Get document metadata by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/{document_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def delete(document_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Delete a document by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/{document_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}") 