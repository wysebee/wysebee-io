import typer
from colorama import init as colorama_init, Fore
from pathlib import Path 

colorama_init(autoreset=True)
app = typer.Typer()


@app.command()
def init(name: str):
  print(Fore.GREEN + f"Creating app {name}")
  # Create the main app directory
  app_dir = Path(name)
  app_dir.mkdir(parents=True, exist_ok=True)
  
  # Create the src subfolder
  src_dir = app_dir / "src"
  src_dir.mkdir(exist_ok=True)
  print(Fore.BLUE + f"Created src folder in {name}")

  # Create the ui subfolder
  ui_dir = app_dir / "ui"
  ui_dir.mkdir(exist_ok=True)
  print(Fore.BLUE + f"Created ui folder in {name}")

  # Create main.py file with main() function
  main_file = src_dir / "main.py"
  main_file.write_text('''def main():
    print("Hello from Wysebee App!")

if __name__ == "__main__":
    main()
''')
  print(Fore.BLUE + f"Created main.py file in {name}/src")


@app.command()
def dev():
  typer.echo(f"Running app in dev mode!")

@app.command()
def build():
  typer.echo(f"Building app!")

if __name__ == "__main__":
  app()