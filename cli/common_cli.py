import typer
import requests

app = typer.Typer(help="Common utility commands.")

API_URL = "http://localhost:8000"

@app.command()
def health():
    """Check API and database health."""
    response = requests.get(f"{API_URL}/health")
    typer.echo(response.json() if response.ok else f"Error: {response.status_code} - {response.text}") 