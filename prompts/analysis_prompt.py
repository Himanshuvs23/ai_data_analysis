# Import Libraries
import textwrap
from typing import List, Dict

def sensitive_columns_prompt(
    column_names: List[str],
    column_descriptions: Dict[str, str]
) -> str:
    columns_block = "\n".join(
        f"- {name}: {column_descriptions.get(name, 'No description available')}"
        for name in column_names
    )

    return textwrap.dedent(f"""
    You are a data privacy classifier.

    Identify columns that likely contain sensitive or personally identifiable information (PII).

    Examples: names, emails, phone numbers, SSN, addresses, dates of birth,
    medical info, salary, bank accounts, credit cards, geolocation.

    Use both the column name and its description to make your judgment. A column
    with an ambiguous or generic name (e.g. "x7") may still be sensitive if its
    description indicates it contains PII. If uncertain whether a column is
    sensitive, include it rather than omit it.

    Return ONLY a valid JSON array of sensitive column names.
    No explanation, no markdown, no preamble.
    If none found, return an empty array.

    Columns (name: description):
    {columns_block}
    """).strip()


def identifier_columns_prompt(
    column_names: List[str],
    column_descriptions: Dict[str, str]
) -> str:
    columns_block = "\n".join(
        f"- {name}: {column_descriptions.get(name, 'No description available')}"
        for name in column_names
    )

    return textwrap.dedent(f"""
    You are a data analyst classifier.

    Identify columns that likely function as identifiers rather than analytical features.

    Examples: customer IDs, passenger IDs, employee IDs, order IDs, UUIDs,
    usernames, account IDs, record numbers, names used to uniquely identify individuals.

    Use both the column name and its description to make your judgment. A column
    with an ambiguous or generic name may still be an identifier if its description
    indicates it uniquely identifies a record or entity.

    Return ONLY a valid JSON array of identifier column names.
    No explanation, no markdown, no preamble.
    If none found, return an empty array.

    Columns (name: description):
    {columns_block}
    """).strip()