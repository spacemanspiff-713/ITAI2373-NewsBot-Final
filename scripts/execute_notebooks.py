from pathlib import Path
import nbformat
from nbclient import NotebookClient
root=Path(__file__).resolve().parents[1]
for path in sorted((root/"notebooks").glob("0[1-7]_*.ipynb")):
    notebook=nbformat.read(path,as_version=4); NotebookClient(notebook,timeout=180,kernel_name="python3").execute(cwd=str(root)); nbformat.write(notebook,path); print(f"Executed {path.name}")
