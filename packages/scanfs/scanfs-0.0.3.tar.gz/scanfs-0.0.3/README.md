# scanfs

This module scans the filesystem and provides custom hooks to handle each file
type of your choice.

## Installation

```bash
pip install scanfs
```

## Example

```python
def callback(fpath, node):
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

fss = FileSystemScanner("/usr/bin")
fss.checksec_on_elfs()
```

## Developer

```bash
python setup.py bdist_wheel sdist
twine upload dist/*
```
