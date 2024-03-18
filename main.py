import os

import click

@click.group()
def cs50_cli():
    """
    function that serves a groups
    """
    pass

@cs50_cli.command("degree")
@click.option("--start", "-s", "start", type=str)
@click.option("--end", "-e", "end", type=str)
def degrees(start: str, end: str):
    from degrees import Degree, load_data

    #loading data
    directory = os.path.dirname(__file__) + "/data/large"
    load_data(directory=directory)
    d = Degree()
    result = d.solve(start=start, goal=end)
    print(result)


if __name__ == "__main__":
    cs50_cli()