from decimal import Context
from src.filesystemscanner import FileSystemScanner, FileSystemScannerException
import pytest


def test_empty_fwpath():
    with pytest.raises(FileSystemScannerException) as context:
        fss = FileSystemScanner("")
    # assert context.value == "Folder path is empty"


def test_fwpath_notstr():
    with pytest.raises(FileSystemScannerException) as context:
        fss = FileSystemScanner(10)

    print(context.value)
    # assert context.value == "Folder path is not type string"
