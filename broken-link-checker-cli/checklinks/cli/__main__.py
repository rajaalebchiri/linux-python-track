from ..core import get_links
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()

@app.command()
def check_links_table(file_path: str):
    lines = get_links(file_path)
    console = Console()
    table = Table(title="Links Status Table")
    table.add_column("Link", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")

    for line in lines:
        table.add_row(line['href'], str(line['status']))

    console.print(table)


if __name__ == "__main__":
    app()