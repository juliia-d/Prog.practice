import typer
from typing import List, Optional

app = typer.Typer()

def read_numbers_from_file():
    numbers = []
    with open("file", "r") as f:  
        for line in f:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers


def write_output(result):
    with open("output", "w") as f:
        f.write(str(result))


@app.command()
def main(
    numbers: Optional[List[int]] = typer.Argument(None, help="Numbers to sum"),
    file: bool = typer.Option(False, "-f", help="Read numbers from file"),
    output: bool = typer.Option(False, "-o", help="Write result to output file"),
):

    
    if file:
        numbers = read_numbers_from_file()
    elif numbers is None:
        numbers = []

    result = sum(numbers)

    
    if output:
        write_output(result)
    else:
        typer.echo(result)


if __name__ == "__main__":
    app()

