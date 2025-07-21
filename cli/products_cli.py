import typer
import requests
from typing import Optional

app = typer.Typer(help="Products & Stock management commands.")

API_URL = "http://localhost:8000/api/v1"

# Products
@app.command()
def list_products(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/products", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_product(code_produit: str = typer.Option(..., prompt=True), nom: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"code_produit": code_produit, "nom": nom}
    response = requests.post(f"{API_URL}/products", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_product(product_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/products/{product_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def update_product(product_id: int, code_produit: Optional[str] = None, nom: Optional[str] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {k: v for k, v in locals().items() if k not in ("product_id", "token") and v is not None}
    response = requests.patch(f"{API_URL}/products/{product_id}", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def add_supplier(product_id: int, entreprise_id: int, qty: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"entreprise_id": entreprise_id, "qty": qty}
    response = requests.post(f"{API_URL}/products/{product_id}/suppliers", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def remove_supplier(product_id: int, supplier_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/products/{product_id}/suppliers/{supplier_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

# Articles
@app.command()
def list_articles(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/articles", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_article(id_produit: int = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"id_produit": id_produit}
    response = requests.post(f"{API_URL}/articles", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_article(article_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/articles/{article_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

# Stocks
@app.command()
def list_stocks(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/stocks", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_stock(libelle: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"libelle": libelle}
    response = requests.post(f"{API_URL}/stocks", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_stock(stock_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/stocks/{stock_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_inventory(stock_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/stocks/{stock_id}/inventory", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

# Stock Moves
@app.command()
def create_stock_move(id_article: int = typer.Option(..., prompt=True), src_stock: Optional[int] = None, dst_stock: Optional[int] = None, qty: int = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"id_article": id_article, "qty": qty}
    if src_stock:
        data["src_stock"] = src_stock
    if dst_stock:
        data["dst_stock"] = dst_stock
    response = requests.post(f"{API_URL}/stock-moves", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_stock_move(move_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/stock-moves/{move_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 