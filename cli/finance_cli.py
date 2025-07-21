import typer
import requests
from typing import Optional

app = typer.Typer(help="Finance management commands.")

API_URL = "http://localhost:8000/api/v1"

# Accounts
@app.command()
def list_accounts(page: int = 1, page_size: int = 10, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    response = requests.get(f"{API_URL}/ledger/accounts", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_account(libelle: str = typer.Option(..., prompt=True), account_type: str = typer.Option(..., prompt=True), token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"libelle": libelle, "account_type": account_type}
    response = requests.post(f"{API_URL}/ledger/accounts", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_account(account_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/ledger/accounts/{account_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

# Ledger Lines
@app.command()
def list_ledger_lines(page: int = 1, page_size: int = 10, account_id: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "page_size": page_size}
    if account_id:
        params["account_id"] = account_id
    response = requests.get(f"{API_URL}/ledger/lines", headers=headers, params=params)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def create_ledger_line(debit_account: int = typer.Option(..., prompt=True), credit_account: int = typer.Option(..., prompt=True), amount_minor: int = typer.Option(..., prompt=True), id_cat: Optional[int] = None, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"debit_account": debit_account, "credit_account": credit_account, "amount_minor": amount_minor}
    if id_cat:
        data["id_cat"] = id_cat
    response = requests.post(f"{API_URL}/ledger/lines", headers=headers, json=data)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def get_ledger_line(line_id: int, token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/ledger/lines/{line_id}", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

# Reports
@app.command()
def trial_balance(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/ledger/balance", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}")

@app.command()
def profit_loss(token: str = typer.Option(..., prompt=True, hide_input=True)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/ledger/profit-loss", headers=headers)
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 