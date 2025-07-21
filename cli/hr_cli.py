import typer
import requests
from typing import Optional
from auth_manager import get_auth_header

app = typer.Typer(help="Human Resources commands.")

API_URL = "http://localhost:8000/api/v1"

@app.command()
def list_employees(page: int = 1, page_size: int = 10, token: Optional[str] = None):
    headers = get_auth_header(token)
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/employees", headers=headers, params=params)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def create_employee(cin_numero: str = typer.Option(..., prompt=True), nom: str = typer.Option(..., prompt=True), prenom: str = typer.Option(..., prompt=True), etat_civil: str = typer.Option(..., prompt=True), date_naissance: str = typer.Option(..., prompt=True), salaire_net: float = typer.Option(..., prompt=True), id_fonction: int = typer.Option(..., prompt=True), email: Optional[str] = typer.Option(None), password: Optional[str] = typer.Option(None, hide_input=True), role: Optional[str] = typer.Option(None), token: Optional[str] = None):
    headers = get_auth_header(token)
    data = {
        "cin_numero": cin_numero,
        "nom": nom,
        "prenom": prenom,
        "etat_civil": etat_civil,
        "date_naissance": date_naissance,
        "salaire_net": salaire_net,
        "id_fonction": id_fonction,
        "email": email,
        "password": password,
        "role": role
    }
    # The create employee endpoint is just /api/v1 (not /api/v1/employees)
    response = requests.post(f"{API_URL}", headers=headers, json=data)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def get_employee(employee_id: int, token: Optional[str] = None):
    headers = get_auth_header(token)
    response = requests.get(f"{API_URL}/employees/{employee_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def update_employee(employee_id: int, nom: Optional[str] = None, prenom: Optional[str] = None, etat_civil: Optional[str] = None, date_naissance: Optional[str] = None, salaire_net: Optional[float] = None, id_fonction: Optional[int] = None, email: Optional[str] = None, password: Optional[str] = None, role: Optional[str] = None, token: Optional[str] = None):
    headers = get_auth_header(token)
    data = {k: v for k, v in locals().items() if k not in ("employee_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/employees/{employee_id}", headers=headers, json=data)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def delete_employee(employee_id: int, token: Optional[str] = None):
    headers = get_auth_header(token)
    response = requests.delete(f"{API_URL}/employees/{employee_id}", headers=headers)
    if response.ok:
        typer.echo(response.json())
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}") 