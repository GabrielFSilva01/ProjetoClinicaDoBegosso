
import os

class GerenciadorArquivo:
   
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def gravar_registro(self, registro_formatado):
       
        with open(self.nome_arquivo, 'a+', encoding='utf-8') as f:
            # tell() retorna o endereço (offset) atual (o início da nova gravação)
            endereco_byte = f.tell() 
            
            if not registro_formatado.endswith('\n'):
                registro_formatado += '\n'
            
            f.write(registro_formatado)
            
            return endereco_byte

    def ler_registro_por_endereco(self, endereco_byte):
       
        try:
            with open(self.nome_arquivo, 'r', encoding='utf-8') as f:
              
                f.seek(endereco_byte)
                registro = f.readline().strip() 
                
                
                if registro and registro.startswith('*'):
                    return None 
                
                return registro
        except FileNotFoundError:
            return None 

    def excluir_registro(self, endereco_byte):
        try:
            # r+ permite leitura e escrita (sobrescrita)
            with open(self.nome_arquivo, 'r+', encoding='utf-8') as f:
                f.seek(endereco_byte)
                f.write('*') 
            return True
        except Exception:
            return False

    def ler_arquivo_exaustivo(self):
      
        registros = []
        try:
            with open(self.nome_arquivo, 'r', encoding='utf-8') as f:
                f.seek(0)
                for linha in f:
                    registro = linha.strip()
                 
                    if registro and not registro.startswith('*'):
                        registros.append(registro)
            return registros
        except FileNotFoundError:
            return []