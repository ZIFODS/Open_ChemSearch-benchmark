import pytest

from chemsearch import urls
from chemsearch.constants import Queries


class TestConstructSubstructureSearchUrl:
    def test_completes(self):
        urls.construct_substructure_search_url(
            "127.0.0.1", 8000, "c1ccccc1", Queries.SMILES, True
        )

    @pytest.mark.parametrize(
        "query, query_type, persist, expected",
        [
            (
                "c1ccccc1",
                Queries.SMILES,
                True,
                "http://127.0.0.1:8000/substructure-search?smiles=c1ccccc1&persist=True",
            ),
            (
                "Fc1ccc(Cn2c(NC3CCNCC3)nc3ccccc32)cc1",
                Queries.SMILES,
                True,
                "http://127.0.0.1:8000/substructure-search?smiles=Fc1ccc%28Cn2c%28NC3CCNCC3%29nc3ccccc32%29cc1&persist=True",
            ),
            (
                "c1ccccc1",
                Queries.SMARTS,
                True,
                "http://127.0.0.1:8000/substructure-search?smarts=c1ccccc1&persist=True",
            ),
            (
                "c1ccccc1",
                Queries.SMARTS,
                False,
                "http://127.0.0.1:8000/substructure-search?smarts=c1ccccc1&persist=False",
            ),
        ],
    )
    def test_returns_expected_url(self, mocker, query, query_type, persist, expected):
        mock = mocker.patch.object(urls, "URLPaths", autospec=True)
        mock.SUBSTRUCTURE_SEARCH = "/substructure-search"

        actual = urls.construct_substructure_search_url(
            "127.0.0.1", 8000, query, query_type, persist
        )

        assert actual == expected
