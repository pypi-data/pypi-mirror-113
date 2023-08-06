import os

import pandas as pd
from babel.numbers import format_currency, format_decimal

from notify.exceptions import EnvironmentVariablesError


def format_numbers(df: pd.DataFrame, currency_columns: list = None, number_columns: list = None):
    """
    Deze functie converteerd currency (bedrag) en number (getal) kolommen naar geformatteerde tekstvelden.

    Parameters
    ----------
    df: pd.DataFrame
        dataset waarin kolommen staan die geconverteerd dienen te worden
    currency_columns: list
        lijst met kolomnamen die geconverteerd worden naar € kolommen en formats.
    number_columns: list
        lijst met kolomnamen die geconverteerd worden naar nummer kolommen met nederlandse annotatie.

    Returns
    -------
    df: pd.DataFrame
        dataset met kolommen die gebruikt kunnen worden voor het presenteren van
        bedragen en nummers (locale=NL).
    """

    # format de bedrag kolommen
    if number_columns is None:
        number_columns = []

    if currency_columns is None:
        currency_columns = []

    for col in currency_columns:
        df[col] = df[col].apply(lambda x: format_currency(number=x, currency="EUR", locale="nl_NL"))

    # format de nummer kolommen
    for col in number_columns:
        df[col] = df[col].apply(lambda x: format_decimal(number=x, locale="nl_NL"))

    return df


def check_environment_variables(required_variables: list):
    """
    Parameters
    ----------
    required_variables: list
        list of required variables that need to be present in environment variables.

    Returns
    -------

    """
    # Test if environment variables are set.

    values = [os.environ.get(x) for x in required_variables]

    if not all(values):
        raise EnvironmentVariablesError(f"One of the environment variables {', '.join(required_variables)} is not set")


def dataframe_to_html(df: pd.DataFrame) -> str:
    """
    Deze functie zet een dataframe om in een opgemaakte HTML table. Wanneer de gebruiker zelfstandig een HTML bericht
    opbouwt, kan deze functie uitkomst bieden voor het invoegen van html tabellen.

    Parameters
    ----------
    df: pd.DataFrame
        dataframe die in een HTML table geconverteerd dient te worden.

    Returns
    -------
    pretty_html_table: str
        html body voor de gegeneerde HTML tabel
    """

    html_table = df.to_html(index=False, classes="styled-table", justify="center")

    pretty_html_table = (
        """
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Dataframe report</title>
            <style type="text/css" media="screen">
                h1 {
                    background-color: #a8a8a8;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    text-align: center;
                }

                .styled-table {
                    border-collapse: collapse;
                    margin: 25px 0;
                    font-size: 0.9em;
                    font-family: sans-serif;
                    min-width: 400px;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                }

                .styled-table thead tr {
                    background-color: #009879;
                    color: #ffffff;
                    text-align: left;
                }

                .styled-table th,
                .styled-table td {
                    padding: 12px 15px;
                }

                .styled-table tbody tr {
                    border-bottom: thin solid #dddddd;
                }

                .styled-table tbody tr:nth-of-type(even) {
                    background-color: #f3f3f3;
                }

                .styled-table tbody tr.active-row {
                    font-weight: bold;
                    color: #009879;
                }

                .styled-table tbody tr:last-of-type {
                    border-bottom: 2px solid #009879;
                }
            </style>
        </head>
        <body>"""
        + html_table
        + "</body>"
    )

    return pretty_html_table
