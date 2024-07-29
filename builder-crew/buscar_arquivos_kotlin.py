
from pathlib import Path

# Retorna um unico arquivo por vez/call
def buscar_arquivo_original_com_erro(directory_path: str, log: bool):
    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.suffix == '.kt':  # Check if it's a text file
            with file_path.open('r') as file:
                content = file.read()
                if (log):
                    print(f"Conteúdo do arquivo {file_path.name}:")
                    print(content)
                return(content)


if __name__ == "__main__":
    directory_path = Path('running-crew/kotlin-files')
    buscar_arquivo_original_com_erro(directory_path=directory_path, log=True)