from typing import Optional, List

import click
import os
import pandas as pd


file_generated = os.getenv("FILE_GENERATED", None)
file_import = os.getenv("FILE_IMPORT", None)
class_template = os.getenv("CLASS_TEMPLATE", None)
test_case_template = os.getenv("TEST_CASE_TEMPLATE", None)


def is_invalid_env() -> bool:
    if file_generated is None:
        click.echo(click.style("ERROR: Please set environment variable: FILE_GENERATED", fg="red"))
        return True
    if class_template is None:
        click.echo(click.style("ERROR: Please set environment variable: CLASS_TEMPLATE", fg="red"))
        return True
    if test_case_template is None:
        click.echo(click.style("ERROR: Please set environment variable: TEST_CASE_TEMPLATE", fg="red"))
        return True
    if file_import is None:
        click.echo(click.style("ERROR: Please set environment variable: FILE_IMPORT", fg="red"))
        return True
    if not file_import.endswith(".xlsx"):
        click.echo(click.style("ERROR: Only support .xlsx file", fg="red"))
        return True
    return False


def get_test_names() -> Optional[List[str]]:
    try:
        dfs = pd.read_excel(io=file_import)
        titles = tuple(dfs.columns)
        if "NAME" not in titles:
            click.echo(click.style("ERROR: Invalid file, column NAME is required", fg="red"))
            return None
        col = titles.index("NAME")
        total_rows = len(dfs.values)
        test_names: List[str] = list()
        for row in range(0, total_rows):
            test_name = str(dfs.values[row][col])
            if test_name is None or test_name == 'nan' or len(test_name.strip()) == 0:
                continue
            test_names.append(test_name)
        return test_names
    except FileNotFoundError:
        click.echo(click.style("ERROR: File not found", fg="red"))


def write_to_file(content: str):
    f = open(file_generated, "w")
    f.write(content)
    f.close()


def get_class_template() -> str:
    f = open(class_template, "r")
    template = f.read()
    f.close()
    return template


def get_test_case_template() -> str:
    f = open(test_case_template, "r")
    template = f.read()
    f.close()
    return template


@click.command()
def cli():
    if is_invalid_env():
        return

    # validate template
    if "$body$" not in get_class_template():
        click.echo(click.style("ERROR: Invalid class template", fg="red"))
        return True

    if "$test_case_name$" not in get_test_case_template() or "$test_number$" not in get_test_case_template():
        click.echo(click.style("ERROR: Invalid test case template", fg="red"))
        return True

    test_names = get_test_names()
    if not test_names:
        click.echo(click.style("INFO: No test case in imported file", fg="yellow"))
        return
    body = ""
    number = 1
    for test_name in test_names:
        test_case = get_test_case_template().replace("$test_case_name$", test_name).replace("$test_number$", str(number))
        body += test_case
        number += 1
    write_to_file(get_class_template().replace("$body$", body))
    click.echo(click.style(f"SUCCESS: Import test case to {file_generated} success", fg="green"))
