import typer
import requests
from typing import Optional

app = typer.Typer(help="Reference data management commands.")

API_URL = "http://localhost:8000/api/v1"

@app.command()
def list_devises(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/devise", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_devise(code: str = typer.Option(..., prompt=True), libelle: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"code": code, "libelle": libelle}
    response = requests.post(f"{API_URL}/devise", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def list_expense_categories(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/expense-categories", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_expense_category(libelle: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"libelle": libelle}
    response = requests.post(f"{API_URL}/expense-categories", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def list_statuts_fabrication(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/statuts/fabrication", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def list_statuts_livraison(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/statuts/livraison", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def list_statuts_appro(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/statuts/appro", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 