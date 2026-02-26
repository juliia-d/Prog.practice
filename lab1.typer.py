import typer
from typing import List, Optional

app = typer.Typer()

# Функція для читання чисел з файлу
def read_numbers_from_file():
    numbers = []
    with open("file", "r") as f:  # файл з даними
        for line in f:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers

# Функція для запису результату
def write_output(result):
    with open("output", "w") as f:  # файл з результатом
        f.write(str(result))

# Головна функція CLI
@app.command()
def main(
    numbers: Optional[List[int]] = typer.Argument(None, help="Numbers to sum"),
    file: bool = typer.Option(False, "-f", help="Read numbers from file"),
    output: bool = typer.Option(False, "-o", help="Write result to output file"),
):
    """
    Sum integers from command line or from file 'file'.
    """
    # Визначаємо, звідки брати числа
    if file:
        numbers = read_numbers_from_file()
    elif numbers is None:
        numbers = []

    result = sum(numbers)

    # Вивід результату
    if output:
        write_output(result)
    else:
        typer.echo(result)


if __name__ == "__main__":
    app()
