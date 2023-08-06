"""Command-line interface."""
import typer

command_line = typer.Typer()


@command_line.command()
def main(prog_name: str) -> None:
    """Stock Trader."""
    return None


if __name__ == "__main__":
    main(prog_name="stock_trader")  # pragma: no cover
