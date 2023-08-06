import os
import magic
import subprocess
from tqdm import tqdm
from filesystemscannerexception import FileSystemScannerException


class FileSystemScanner:

    """
    FileSystemScanner

    This scanner scans the folder in the filesystem
    with various filetype filters and provides a hook
    whenever the filetype is found in the provided path

    Attributes:
        fpath (str): Folder in the filesytem to scan

    Raises:
        FileSystemScannerException: [Exception when the
        folder path fpath is empty or not valid]
    """

    def __init__(self, fpath: str) -> None:
        super().__init__()
        self._check_str_param(fpath)
        self.fpath = fpath

    def scan_for(self, filetype, callback):
        """
        Scans for specific filetype in the nested folder

        Args:
            filetype ([type]): Filetype
            callback (function): Function called when the filetype
            is found
        """
        nodes = os.scandir(self.fpath)

        for node in tqdm(nodes, desc="Scanning...", unit=" files", unit_scale=1):
            callback(self.fpath, node)

    def scan_for_elfs(self, callback):
        """
        Scans for elf file types in the nested folder

        Args:
            callback (function): Function called when the elf file type
            is found
        """
        nodes = os.scandir(self.fpath)

        try:
            for node in tqdm(
                nodes, desc="Scanning ELF files...", unit=" files", unit_scale=1
            ):
                fpath = os.path.join(self.fpath, node.name)

                if magic.from_file(fpath).find("ELF") != -1 and not node.is_symlink():
                    callback(self.fpath, node)
        except:
            pass  # TODO: Handle the exceptions while scanning directory

    def checksec_dump(self, fpath, node):
        try:
            path = os.path.join(fpath, node.name)
            completed_process = subprocess.run(
                ["checksec", "--format=json", "--file=" + str(path)],
                capture_output=True,
                check=True,
            )
            print(completed_process)
        except Exception as e:
            print("An exception occurred: " + str(e))

    def checksec_on_elfs(self):
        """
        Checks the security features enabled on elf

        Args:
            filename (str): Filename to store the results of checksec in JSON
            format
        """
        self.scan_for_elfs(self.checksec_dump)

    def _check_str_param(self, param):
        if not isinstance(param, str) or not param:
            raise FileSystemScannerException(
                f'Firmware path "{param}" is empty or not valid string!!!'
            )


if __name__ == "__main__":

    files = []

    def callback(fpath, node):
        try:
            path = os.path.join(fpath, node.name)
            completed_process = subprocess.run(
                ["checksec", "--format=json", "--file=" + str(path)],
                capture_output=True,
                check=True,
            )
            # print(completed_process)
            statinfo = os.stat(path)
            files.append(magic.from_file(path))
        except Exception as e:
            print("An exception occurred: " + str(e))

    fss = FileSystemScanner("/usr/bin")
    # fss = FileSystemScanner("/home/maker/Downloads")
    # fss.scan_for_elfs(callback)
    #    print(files)
    fss.checksec_on_elfs()
