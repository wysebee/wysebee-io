import typer

app = typer.Typer()


@app.command()
def init(name: str):
  typer.echo(f"Creating app {name}!")

@app.command()
def dev():
  typer.echo(f"Running app in dev mode!")

@app.command()
def build():
  typer.echo(f"Building app!")

if __name__ == "__main__":
  app()