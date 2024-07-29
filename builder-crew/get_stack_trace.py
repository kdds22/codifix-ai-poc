
import json
import re
from pathlib import Path

# Definir a regex para arquivos .kt
default_pattern = re.compile(r'[A-Za-z]+(?:[A-Za-z0-9]+)*\.kt')
ignore_files = ['CoroutineScheduler.kt', 'DispatchedTask.kt','ZebraRFR8500.kt','ContinuationImpl.kt', 'ReaderManager.kt']

def search_pattern_in_stack_trace(json_data, pattern, key_search):
    matches = []
    # print(f'JsonData: {json_data} - KeySearch: {key_search}')
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == key_search and isinstance(value, str):
                matches.extend(pattern.findall(value))
            elif isinstance(value, list) or isinstance(value, dict):
                matches.extend(search_pattern_in_stack_trace(value, pattern, key_search))
    elif isinstance(json_data, list):
        for item in json_data:
            matches.extend(search_pattern_in_stack_trace(item, pattern, key_search))
    return list(set(matches))

def search_pattern_in_symbol(json_data, pattern, key_search):
    matches = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            # print(f'Key: {key}')
            # print(f'Value: {value}\n')
            for v in value:
                # print(f'key_search_value: {v[key_search]}\n')
                # matches.extend(pattern.findall(v[key_search]))
                matches.append(v[key_search])
    # print(f'Matches: {matches}')
    return list(set(matches))

def get_file_list_error(directory_path: str, log: bool = False):
    print(f'Procurando arquivos nos diretórios... {directory_path}\n')

    list_match_unique = []

    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.suffix == '.json':
            with file_path.open(mode='r', encoding='utf-8') as file:
                content = json.load(file)

                # Buscar o padrão nos 'Stack Trace'
                matches = search_pattern_in_stack_trace(content, default_pattern, "file")
                unique_matches = list(set(matches))
                print(f'Unique_matches: {unique_matches}\n')

                # list_match_unique = []
                # print("Correspondências distintas encontradas nos 'Stack Trace':")
                for match in unique_matches:
                    if (match not in ignore_files):
                        list_match_unique.append(match)


                if (log):
                    print(f"Conteúdo do arquivo {file_path.name}:")
                    print(content)
                    print(f"Arquivios únicos encontrados:")
                    print(list_match_unique)
                # return(content)
    
    # print(f'{len(list(set(list_match_unique)))} arquivos encontrados nos diretórios.\n')
    return list(set(list_match_unique))
    
   

if __name__ == '__main__':
    directory_path = Path('running-crew/erros')
    print(get_file_list_error(directory_path=directory_path, log=False))
    pass


 # with open('erros_por_tipo_20240611115838.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)

    # # Buscar o padrão nos 'Stack Trace'
    # matches = search_pattern_in_stack_trace(data, pattern)
    # unique_matches = list(set(matches))

    # list_match_unique = []
    # print("Correspondências distintas encontradas nos 'Stack Trace':")
    # for match in unique_matches:
    #     if (match not in ignore_files):
    #         list_match_unique.append(match)
    #         # print(match)
    
    # return list_match_unique


# import json
# import re
# import json
# import re

# # Definir a regex
# pattern = re.compile(r'^[A-Za-z]+(?:[A-Za-z0-9]+)*\.kt$')

# # Função para buscar o padrão no JSON
# def search_pattern_in_json(json_data, pattern):
#     matches = []
#     if isinstance(json_data, dict):
#         for key, value in json_data.items():
#             if isinstance(value, str):
#                 if pattern.match(value):
#                     matches.append(value)
#             else:
#                 matches.extend(search_pattern_in_json(value, pattern))
#     elif isinstance(json_data, list):
#         for item in json_data:
#             matches.extend(search_pattern_in_json(item, pattern))
#     return matches


# def get_fatal_stack_trace():
#        with open('erros_por_tipo_20240611115838.json','r') as json_file:
#               json_stack_trace = json.load(json_file)['FATAL'][0]['Stack Trace']
#               print(json_stack_trace)
#        pass 

# def get_non_fatal_stack_trace():
#        with open('erros_por_tipo_20240611115838.json','r') as json_file:
#               # Só está buscando o primeiro item da lista no Json
#               json_stack_trace = json.load(json_file)['NON_FATAL'][0]['Stack Trace']
#               print(json_stack_trace)
#        pass 


# if __name__ == '__main__':
#        #get_fatal_stack_trace()
#        #get_non_fatal_stack_trace()
#         # Ler o arquivo JSON
#     with open('erros_por_tipo_20240611115838.json', 'r') as file:
#         # data = json.load(file)
#         data = json.load(file)['FATAL'][0]['Stack Trace']

#         # Buscar o padrão
#         matches = search_pattern_in_json(data, pattern)

#         # Exibir as correspondências
#         print("Correspondências encontradas:")
#         for match in matches:
#             print(match)
#     pass