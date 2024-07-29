
from . import big_queries
from dotenv import load_dotenv
load_dotenv()

def start_bigquery(directory_path):
    return big_queries.mostrar_erros_por_tipo(directory_path)


if __name__ == "__main__":
    directory_path = 'running-crew/erros'
    result = start_bigquery(directory_path=directory_path)
    print(result)