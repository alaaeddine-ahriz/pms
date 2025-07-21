import typer
import requests
from typing import Optional
from auth_manager import get_auth_header

app = typer.Typer(help="Materials management commands.")

API_URL = "http://localhost:8000/api/v1/materials"

@app.command()
def list(page: int = 1, page_size: int = 10, token: Optional[str] = None):
    headers = get_auth_header(token)
    params = {"page": page, "page_size": page_size}
    response = requests.get(API_URL, headers=headers, params=params)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def create(nom: str = typer.Option(..., prompt=True), id_facture: Optional[int] = typer.Option(None), token: Optional[str] = None):
    headers = get_auth_header(token)
    data = {"nom": nom}
    if id_facture:
        data["id_facture"] = id_facture
    response = requests.post(API_URL, headers=headers, json=data)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def get(material_id: int, token: Optional[str] = None):
    headers = get_auth_header(token)
    response = requests.get(f"{API_URL}/{material_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def update(material_id: int, nom: Optional[str] = None, id_facture: Optional[int] = None, token: Optional[str] = None):
    headers = get_auth_header(token)
    data = {k: v for k, v in locals().items() if k not in ("material_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/{material_id}", headers=headers, json=data)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}") 