import requests
import typer
from dotenv import load_dotenv
from os import getenv, path
from typing import Optional
from rich import print
import sys

load_dotenv()


def get_ignores(pl: str) -> Optional[str]:
    URL: str = f"{getenv('BASE_URL')}{pl}"
    response = requests.get(URL, stream=True)
    ignores: str = ""
    if response.status_code == 200:
        for res in response.iter_lines():
            ignores += f"{res.decode('utf-8')}\n"
    else:
        response.raise_for_status()
    return ignores


def write_gitignore(data: str) -> None:
    with open(".gitignore", "w") as fp:
        fp.write(data)
    print("[bold green]Done.[/bold green] [blue]Git ignore file created[/blue] :boom:")


def main(programming_language: str):
    all_data = get_ignores(programming_language)
    try:
        if not path.isfile(".gitignore"):
            write_gitignore(data=all_data)
            sys.exit(0)
        ans = input("Gitignore file already exist, do you want to write again? (Y/n): ")
        if ans.lower() == "y":
            write_gitignore(data=all_data)
            sys.exit(0)
        elif ans.lower() == "n":
            sys.exit(0)
        else:
            print("[bold red]Invalid answer[/bold red]")
            sys.exit(0)
    except Exception as e:
        print(f"[bold red]Error: {e}[/bold red]")
    print("[bold red]Alert![/bold red] [green]Git ignore file already exist!.[/green]")


if __name__ == "__main__":
    typer.run(main)
