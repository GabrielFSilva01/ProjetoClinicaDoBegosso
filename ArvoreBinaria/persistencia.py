# persistencia.py

import os

class GerenciadorArquivo:
    """Gerencia a leitura e escrita física no arquivo de dados (Área de Dados)."""
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def gravar_registro(self, registro_formatado):
        """Grava no final do arquivo e retorna o endereço de byte (offset)."""
        # 'a+' permite leitura/escrita e garante que a escrita é feita no final (append)
        with open(self.nome_arquivo, 'a+', encoding='utf-8') as f:
            # tell() retorna o endereço (offset) atual (o início da nova gravação)
            endereco_byte = f.tell() 
            
            if not registro_formatado.endswith('\n'):
                registro_formatado += '\n'
            
            f.write(registro_formatado)
            
            return endereco_byte

    def ler_registro_por_endereco(self, endereco_byte):
        """Lê um registro específico usando o endereço fornecido pelo índice."""
        try:
            with open(self.nome_arquivo, 'r', encoding='utf-8') as f:
                # seek() pula o ponteiro diretamente para o endereço
                f.seek(endereco_byte)
                registro = f.readline().strip() 
                
                # Ignora registros marcados com '*' (exclusão lógica)
                if registro and registro.startswith('*'):
                    return None 
                
                return registro
        except FileNotFoundError:
            return None 

    def excluir_registro(self, endereco_byte):
        """
        Implementa a exclusão LÓGICA: marca o registro com '*' no início.
        Isso preserva o endereço e evita a reorganização imediata do arquivo[cite: 101, 103].
        """
        try:
            with open(self.nome_arquivo, 'r+', encoding='utf-8') as f:
                f.seek(endereco_byte)
                f.write('*') # Sobrescreve apenas o primeiro caractere com o marcador de exclusão
            return True
        except Exception:
            return False

    def ler_arquivo_exaustivo(self):
        """Implementa a Leitura Exaustiva de Registros (leitura linha por linha)."""
        registros = []
        try:
            with open(self.nome_arquivo, 'r', encoding='utf-8') as f:
                f.seek(0)
                for linha in f:
                    registro = linha.strip()
                    # Filtra registros logicamente excluídos
                    if registro and not registro.startswith('*'):
                        registros.append(registro)
            return registros
        except FileNotFoundError:
            return []