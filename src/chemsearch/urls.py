import urllib.parse

from chemsearch.constants import Queries, URLPaths


def construct_substructure_search_url(
    ip_address: str, port: int, query: str, query_type: Queries, persist: bool
) -> str:
    """Construct substructure search URL with query from address to running server.

    Args:
        ip_address (str): IP address of server.
        port (int): Port of server.
        query (str): Query string.
        query_type (Queries): Query type.
        persist (bool): Persist hits in SMI file.

    Returns:
        str: URL.
    """
    query = urllib.parse.urlencode({query_type: query, "persist": persist})

    components = (
        "http",
        f"{ip_address}:{port}",
        URLPaths.SUBSTRUCTURE_SEARCH,
        None,
        query,
        None,
    )

    url = urllib.parse.urlunparse(components)

    return url
