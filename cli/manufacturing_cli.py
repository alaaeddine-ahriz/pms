import typer
import requests
from typing import Optional

app = typer.Typer(help="Manufacturing management commands.")

API_URL = "http://localhost:8000/api/v1"

@app.command()
def list_bom(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """List BOMs with pagination."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/bom", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_bom(nom: str = typer.Option(..., prompt=True), description: Optional[str] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Create a new BOM."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"nom": nom}
    if description:
        data["description"] = description
    response = requests.post(f"{API_URL}/bom", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_bom(bom_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Get a BOM by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/bom/{bom_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_bom(bom_id: int, nom: Optional[str] = None, description: Optional[str] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Update a BOM by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("bom_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/bom/{bom_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def add_bom_product(bom_id: int, product_id: int, qty: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Add a product to a BOM."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"product_id": product_id, "qty": qty}
    response = requests.post(f"{API_URL}/bom/{bom_id}/products", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def list_orders(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """List fabrication orders with pagination."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/orders/fabrication", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_order(id_projet: Optional[int] = None, id_statut_fabrication: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Create a new fabrication order."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {}
    if id_projet:
        data["id_projet"] = id_projet
    if id_statut_fabrication:
        data["id_statut_fabrication"] = id_statut_fabrication
    response = requests.post(f"{API_URL}/orders/fabrication", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_order(order_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Get a fabrication order by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/orders/fabrication/{order_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_order(order_id: int, id_projet: Optional[int] = None, id_statut_fabrication: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Update a fabrication order by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("order_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/orders/fabrication/{order_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def link_bom(order_id: int, nomenclature_id: int, qty: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Link a BOM to a fabrication order."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"nomenclature_id": nomenclature_id, "qty": qty}
    response = requests.post(f"{API_URL}/orders/fabrication/{order_id}/bom", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def upload_progress(order_id: int, document_ids: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Upload progress photos for a fabrication order (comma-separated document IDs)."""
    headers = {"Authorization": f"Bearer {token}"}
    doc_ids = [int(x) for x in document_ids.split(",") if x.strip()]
    data = {"document_ids": doc_ids}
    response = requests.post(f"{API_URL}/orders/fabrication/{order_id}/documents", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_status(order_id: int, status_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Update the status of a fabrication order."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"status_id": status_id}
    response = requests.patch(f"{API_URL}/orders/fabrication/{order_id}/status", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 