import pytest
from pyprojroot import here

from chemsearch import io


@pytest.fixture
def data_dir():
    return here() / "tests" / "data"


@pytest.fixture
def smiles():
    return [
        "O=C[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO[C@H]1O[C@H](CO[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@H]1O",
        "CCC(C)(C)c1ccc(OCCCCCCN2CCN(c3ccc(C)c(Cl)c3)CC2)cc1",
        "Clc1ccc(N2CCN(C/C=C/c3ccccc3)CC2)nn1",
        "CCOC(=O)c1ccc(N(CC(C)O)CC(C)O)cc1",
        "Fc1ccc(Cn2c(NC3CCNCC3)nc3ccccc32)cc1",
        "CCOc1ccccc1C(=O)N/N=C(\\C)C(=O)O",
        "O=C(CC1C2C=CC=CC2C(=O)N1c1ccc2ccc(Cl)nc2n1)N1CCC2(CC1)OCCO2",
        "Cc1cnc(NC(=O)C2=C(O)c3ccccc3S(=O)(=O)N2C)s1",
        "COc1ccc(-c2nc(C(F)(F)F)sc2-c2ccc(OC)cc2)cc1",
        "Cn1c2c(c3ccccc31)CCN1C[C@@H]3CCCC[C@H]3C[C@@H]21",
    ]


class TestReadSMIFile:
    @pytest.fixture
    def filepath(self, data_dir):
        return data_dir / "sample.smi"

    def test_completes(self, filepath):
        io.read_smi_file(filepath)

    def test_returns_expected_number_of_elements(self, filepath):
        actual = io.read_smi_file(filepath)

        assert len(actual) == 10

    def test_returns_expected_molecules(self, filepath, smiles):
        expected = smiles

        actual = io.read_smi_file(filepath)

        assert actual == expected

    def test_raises_exception_given_no_file(self):
        with pytest.raises(FileNotFoundError):
            io.read_smi_file("unknown.smi")
