import typer
import requests
from typing import Optional

app = typer.Typer(help="Authentication commands.")

API_URL = "http://localhost:8000/auth"

@app.command()
def login(email: str = typer.Option(..., prompt=True), password: str = typer.Option(..., prompt=True, hide_input=True)):
    """Login and get a JWT token."""
    response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def register(email: str = typer.Option(..., prompt=True), password: str = typer.Option(..., prompt=True, hide_input=True), nom: str = typer.Option(..., prompt=True), prenom: str = typer.Option(..., prompt=True)):
    """Register a new user (admin only)."""
    response = requests.post(f"{API_URL}/register", json={"email": email, "password": password, "nom": nom, "prenom": prenom})
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def refresh(refresh_token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Refresh JWT token (not implemented)."""
    response = requests.post(f"{API_URL}/refresh", json={"refresh_token": refresh_token})
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}") 