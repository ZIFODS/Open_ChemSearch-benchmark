from pathlib import Path


def read_smi_file(filepath: Path) -> list[str]:
    """Read all SMILES strings from SMI file.

    Args:
        filepath (Path): Path to SMI file.

    Returns:
        list[str]: SMILES strings.
    """
    iterator = SMIMolIter(filepath)

    return [smiles for smiles in iterator]


class SMIMolIter:
    """SMI File iterator.

    Returns one SMILES string at a time.
    """

    def __init__(self, path):
        self._path = path
        self._size = self._get_dataset_size()

    def __len__(self):
        return self._size

    def __iter__(self):
        return self._get_generator()

    def _get_dataset_size(self):
        size = 0
        with open(self._path) as f:
            for _ in f:
                size += 1
        return size

    def _get_generator(self):
        with open(self._path) as f:
            for line in f:
                smiles = line.split("\t")[0].strip("\n")
                yield smiles
