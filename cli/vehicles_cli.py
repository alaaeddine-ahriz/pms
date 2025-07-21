import typer
import requests
from typing import Optional

app = typer.Typer(help="Vehicles management commands.")

API_URL = "http://localhost:8000/api/v1"

@app.command()
def list_vehicles(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/vehicles", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_vehicle(immatriculation: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"immatriculation": immatriculation}
    response = requests.post(f"{API_URL}/vehicles", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_vehicle(vehicle_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/vehicles/{vehicle_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_vehicle(vehicle_id: int, immatriculation: Optional[str] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("vehicle_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/vehicles/{vehicle_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def add_km_log(vehicle_id: int, date_releve: str = typer.Option(..., prompt=True), km: int = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"date_releve": date_releve, "km": km}
    response = requests.post(f"{API_URL}/vehicles/{vehicle_id}/km-log", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def assign_driver(vehicle_id: int, employe_id: int = typer.Option(..., prompt=True), date_start: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"employe_id": employe_id, "date_start": date_start}
    response = requests.post(f"{API_URL}/vehicles/{vehicle_id}/drivers", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def close_driver_assignment(vehicle_id: int, employee_id: int, date_end: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"date_end": date_end}
    response = requests.patch(f"{API_URL}/vehicles/{vehicle_id}/drivers/{employee_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 