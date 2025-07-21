import typer
import requests
from typing import Optional

app = typer.Typer(help="Logistics management commands.")

API_URL = "http://localhost:8000/api/v1"

# Deliveries
@app.command()
def list_deliveries(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/deliveries", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_delivery(id_move_out: Optional[int] = None, id_move_in: Optional[int] = None, id_statut_livraison: Optional[int] = None, id_livreur: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("token",) and v is not None}
    response = requests.post(f"{API_URL}/deliveries", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_delivery(delivery_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/deliveries/{delivery_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_delivery(delivery_id: int, id_move_out: Optional[int] = None, id_move_in: Optional[int] = None, id_statut_livraison: Optional[int] = None, id_livreur: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("delivery_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/deliveries/{delivery_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_delivery_status(delivery_id: int, status_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"status_id": status_id}
    response = requests.patch(f"{API_URL}/deliveries/{delivery_id}/status", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

# Supply Requests
@app.command()
def list_supply_requests(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/supply-requests", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_supply_request(id_demandeur: Optional[int] = None, id_statut_appro: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("token",) and v is not None}
    response = requests.post(f"{API_URL}/supply-requests", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_supply_request(request_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/supply-requests/{request_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_supply_request(request_id: int, id_demandeur: Optional[int] = None, id_statut_appro: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("request_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/supply-requests/{request_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def add_supply_request_product(request_id: int, product_id: int, qty: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"product_id": product_id, "qty": qty}
    response = requests.post(f"{API_URL}/supply-requests/{request_id}/products", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def add_supply_request_tracking(request_id: int, id_statut: int, commentaire: Optional[str] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"id_statut": id_statut}
    if commentaire:
        data["commentaire"] = commentaire
    response = requests.post(f"{API_URL}/supply-requests/{request_id}/tracking", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 