import typer
from colorama import init as colorama_init, Fore
from pathlib import Path
import subprocess
import os
import re
import shutil
import webbrowser

colorama_init(autoreset=True)
app = typer.Typer()


def generate_ui_template(name: str, ui_dir: str, template: str):
    # Change to UI directory and initialize vite
    try:
        print(Fore.YELLOW + f"Setting up Vite in UI folder...")
        original_dir = os.getcwd()
        os.chdir(ui_dir)
        if template:
            subprocess.run(
                ["npm", "create", "vite@latest", ".", "--", "--template", template],
                check=True,
            )
        else:
            subprocess.run(
                [
                    "npm",
                    "create",
                    "vite@latest",
                    ".",
                ],
                check=True,
            )

        # Modify vite.config.js to add custom configuration
        vite_config_path = Path("vite.config.js")
        if vite_config_path.exists():
            print(Fore.YELLOW + f"Updating vite.config.js with custom settings...")

            # Read the current content
            config_content = vite_config_path.read_text()

            # Find the defineConfig object
            if "defineConfig" in config_content and "{" in config_content:
                # Insert our custom config before the closing bracket of defineConfig
                # Find the last closing bracket
                if re.search(r"defineConfig\s*\(\s*{", config_content):
                    # Replace the closing parenthesis with our config options plus a closing parenthesis
                    modified_content = re.sub(
                        r"(\s*}\s*\))(?!\s*[,;])",
                        r"""
  base: './',
  build: {
    outDir: 'templates',
  },
\1""",
                        config_content,
                        count=1,
                    )

                    # Write the modified content back
                    vite_config_path.write_text(modified_content)
                    print(
                        Fore.YELLOW
                        + f"Updated vite.config.js with custom configuration"
                    )
        else:
            print(Fore.YELLOW + f"vite.config.js not found, creating it for vanilla template...")
            # Create a new vite.config.js file
            vite_config_path.write_text(
                """import { defineConfig } from 'vite'
// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  build: {
    outDir: 'templates',
    emptyOutDir: true, // Optional: Clears the directory before building
  },
})
"""
            )

        index_html_path = Path("index.html")
        if template == "react":
            index_html_path.write_text(
                """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/vite.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Vite + React</title>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>
        new QWebChannel(qt.webChannelTransport, function(channel) {
            console.log("✅ QWebChannel initialized");
            channel.objects.wysebee.sendMessage("Hello from the frontend!");
            window.wysebee = channel.objects.wysebee;
        });
        </script>
        <script type="module" src="/src/main.jsx"></script>
    </body>
    </html>
    """
            )
        elif template == "react-ts":
            index_html_path.write_text(
                """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/vite.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Vite + React</title>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>
        new QWebChannel(qt.webChannelTransport, function(channel) {
            console.log("✅ QWebChannel initialized");
            channel.objects.wysebee.sendMessage("Hello from the frontend!");
            window.wysebee = channel.objects.wysebee;
        });
        </script>
        <script type="module" src="/src/main.tsx"></script>
    </body>
    </html>
    """
            )
        elif template == "vanilla":
            index_html_path.write_text(
                """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/vite.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Vite + React</title>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>
        new QWebChannel(qt.webChannelTransport, function(channel) {
            console.log("✅ QWebChannel initialized");
            channel.objects.wysebee.sendMessage("Hello from the frontend!");
            window.wysebee = channel.objects.wysebee;
        });
        </script>
        <script type="module" src="/src/main.js"></script>
    </body>
    </html>
    """
            )
        elif template == "vanilla-ts":
            index_html_path.write_text(
                """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/vite.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Vite + React</title>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>
        new QWebChannel(qt.webChannelTransport, function(channel) {
            console.log("✅ QWebChannel initialized");
            channel.objects.wysebee.sendMessage("Hello from the frontend!");
            window.wysebee = channel.objects.wysebee;
        });
        </script>
        <script type="module" src="/src/main.ts"></script>
    </body>
    </html>
    """
            )

        subprocess.run(["npm", "install"], check=True)
        subprocess.run(["npm", "run", "build"], check=True)
        os.chdir(original_dir)
        print(Fore.YELLOW + f"Successfully set up Vite in {name}/ui!")
        print(Fore.GREEN + f"Now you are ready!")
        print(Fore.GREEN + f" To run the app, use:")
        if name != ".":
            print(Fore.GREEN + f"   cd {name}")
        print(Fore.GREEN + f"   python main.py")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error running npm create vite: {e}")
        os.chdir(original_dir)
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")
        os.chdir(original_dir)


@app.command()
def init(
    name: str,
    template: str = typer.Option(
        "react", "--template", help="Template to use: react, react-ts, vanilla, vanilla-ts"
    )
):
    if not template in ["react", "react-ts", "vanilla", "vanilla-ts"]:
        print(
            Fore.RED
            + f"Invalid template '{template}'. Please choose from: react, react-ts, vanilla, vanilla-ts"
        )
        raise typer.Exit(code=1)
    print(Fore.YELLOW + f"Creating app {name}")
    # Create the main app directory
    app_dir = Path(name)
    app_dir.mkdir(parents=True, exist_ok=True)

    # Create the src subfolder
    src_dir = app_dir / "src"
    src_dir.mkdir(exist_ok=True)
    print(Fore.YELLOW + f"Created src folder in {name}")

    # Create the ui subfolder
    ui_dir = app_dir / "ui"
    ui_dir.mkdir(exist_ok=True)
    print(Fore.YELLOW + f"Created ui folder in {name}")

    # Create main.py file with main() function
    main_file = app_dir / "main.py"
    main_file.write_text(
        """
import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from Wysebee import Wysebee

def main():
    app = QApplication(sys.argv)
    wysebee = Wysebee(app)
    wysebee.initialize_window(width=1280, height=800)
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui/templates/index.html"))
    wysebee.launch(html_path)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
"""
    )
    print(Fore.YELLOW + f"Created main.py file in {name}/src")

    requirements_file = app_dir / "requirements.txt"
    requirements_file.write_text(
        """
PySide6
Wysebee
"""
    )
    generate_ui_template(name, ui_dir, template)


@app.command()
def dev():
    build_ui()
    process = subprocess.Popen(
        ["python", "main.py", "--dev"],
    )
    try:
        # Wait for the process to complete
        process.wait()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Stopping development server...")
        process.terminate()


def build_ui():
    original_dir = os.getcwd()
    app_dir = Path(original_dir)
    app_name = app_dir.name
    print(Fore.GREEN + f"Building UI for {app_name}!")

    ui_dir = app_dir / "ui"
    if ui_dir.exists():
        os.chdir(ui_dir)
        try:
            subprocess.run(["npm", "run", "build"], check=True)
            print(Fore.GREEN + f"Successfully built UI for {app_name}!")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error building UI: {e}")
        finally:
            os.chdir(original_dir)
    else:
        print(
            Fore.RED
            + f"UI directory not found at {ui_dir}. Make sure you're in the correct project directory."
        )


@app.command()
def build(ui: bool = typer.Option(False, "--ui", help="Only build the UI portion")):
    if ui:
        build_ui()
    else:
        typer.echo(f"Building app!")
        # Add full build logic here


if __name__ == "__main__":
    app()
