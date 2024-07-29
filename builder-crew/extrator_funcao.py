
import regex
import re
import json
import get_stack_trace

def extract_kotlin_method(file_path, method_name):
    print(f'Verificando o método: {method_name} no arquivo: {file_path.name} .\n')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
    
    # pattern = rf"\b(?:public|private|protected)?\s*fun\s+{re.escape(method_name)}\s*\((.*?)\)\s*{{"
    pattern = rf"{re.escape(method_name)}"
    match = re.search(pattern, file_content, re.DOTALL)
    print(f'Match Pattern file content: {match}')
    if not match:
        return None

    start_index = match.end() - 1
    open_braces = 1
    i = start_index

    print(f'Start Index')
    while i < len(file_content) and open_braces > 0:
        print(i)
        i += 1
        if file_content[i] == '{':
            open_braces += 1
        elif file_content[i] == '}':
            open_braces -= 1

    method_code = file_content[start_index:i+1]
    return method_code

def extrair_metodo_com_erro_por_arquivo(file_directory, method_name):
    print(f'Extraindo método {method_name} com erro.\n')
    erros_por_arquivo = {}
    for file_path in file_directory.iterdir():
        if file_path.is_file() and file_path.suffix == '.kt':
            extracted_method = extract_kotlin_method(file_path, method_name)
            if extracted_method != None:
                if file_path not in erros_por_arquivo:
                    erros_por_arquivo[str(file_path)] = []
                erros_por_arquivo[str(file_path)] = extracted_method
    if len(erros_por_arquivo) == 0:
        return None
    print(f'Erros por arquivo: {erros_por_arquivo}')
    return erros_por_arquivo

def extrair_metodo_do_symbol(symbols_finded_list: list[str]) -> list[str]:
    functions = []
    # print(f'---------------------------------------->   Symbols List: {symbols_finded_list}\n')
    for symbols in symbols_finded_list:
        # print(f'-------------------->   Symbols: {symbols}\n')
        parts = symbols.split('.')
        # print(f'All Parts: {parts}\n')
        # print(f'Function part: {parts[-1]}\n')
        functions.append(parts[-1])
        # for symbol in symbols:
        #     print(f'Symbol: {symbol}\n')
        #     parts = symbol.split('.')
        #     print(f'Parts: {parts}\n')
        #     functions.append(parts[-1])
    result_functions = list(set(functions))
    # print(f'All Functions: {result_functions}\n')
    return result_functions

# Example usage
# qualified_name = 'com.havan.app.abastecimento.data.adapter.abastecimento.AbastecimentoPedidoItemAdapter$ViewHolder.removerCardDaLista'


def erros_encontrados(error_directory, file_directory):
    print('Vinculando erros aos arquivos copiados...\n')
    erros_encontrados = []
    symbols_finded_list = []
    pattern = re.compile(r'^([\w.$]+)\.(\w+)$')
    for file_path in error_directory.iterdir():
        # print(f'File Path: {file_path}\n')
        if file_path.is_file() and file_path.suffix == '.json':
            with file_path.open(mode='r', encoding='utf-8') as json_file:
                content = json.load(json_file)
                # print(f'Conteudo: {content}\n')
                symbol_list = get_stack_trace.search_pattern_in_symbol(content, pattern, 'symbol')
                symbol_list = list(set(symbol_list))
                symbols_finded_list.extend(symbol_list)
                # print(f'Symbol List: {symbol_list}\n')
                # print(f'Symbols Finded List: {symbols_finded_list}\n')
    metodos = extrair_metodo_do_symbol(symbols_finded_list)
    # # print(f'Métodos: {metodos}\n')
    for metodo in metodos:
        # print(f'Método: {metodo}\n')
        erro_encontrado = extrair_metodo_com_erro_por_arquivo(file_directory, metodo)
    #     if erro_encontrado != None:
    #         print(f'Erro encontrado: {erro_encontrado}\n')
    #         if erro_encontrado not in erros_encontrados:
    #             erros_encontrados.append(erro_encontrado)
    print('Erros encontrados: ', erros_encontrados)
    return erros_encontrados


    pass

if __name__ == '__main__':
    file_directory = 'running-crew/kotlin-files' # Exemplo
    method_name = 'removerCardDaLista' # Exemplo
    extracted_method = extrair_metodo_com_erro_por_arquivo(file_directory, method_name)
    print(extracted_method)

