# cidades.py

from ArvoreBinaria.BaseDados import BaseDados

class Cidades(BaseDados):
    """
    Gerencia a tabela Cidades.
    Estrutura: Código da Cidade|Descrição|Estado
    """
    
    def __init__(self):
        # Inicializa o gerenciador para o arquivo 'Cidades.txt' e carrega o índice
        super().__init__('Cidades')

    def incluir_cidade(self, codigo, descricao, estado):
        """Implementa Inclusão (1.1)."""
        # Verifica unicidade
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Cidade com código {codigo} já existe.")
            return False 

        # Formata o registro para persistência em disco
        registro_formatado = f"{codigo}|{descricao}|{estado}"
        
        # Chama o método da BaseDados para salvar no arquivo e no índice
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Cidade {descricao} ({codigo}) incluída.")
        return True
    
    def _deserializar(self, registro_string):
        """Função auxiliar para converter a string do disco em um dicionário."""
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]),
                "descricao": campos[1],
                "estado": campos[2],
            }
        except Exception:
            # Retorna None se a linha estiver corrompida ou mal formatada
            return None

    def consultar_cidade(self, codigo):
        """Implementa Consulta (1.2). Acesso via índice."""
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None
        return self._deserializar(registro_string)

    def listar_todas(self):
        """Implementa Leitura Exaustiva (1.4)."""
        registros_strings = self.ler_todos()
        cidades_listadas = [
            self._deserializar(reg_str) 
            for reg_str in registros_strings 
            if self._deserializar(reg_str) is not None
        ]
        return cidades_listadas

    def excluir_cidade(self, codigo):
        """Implementa Exclusão (1.3) (Exclusão Lógica e remoção do índice)."""
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Cidade {codigo} marcada para exclusão.")
            return True
        else:
            print(f"ERRO: Cidade com código {codigo} não encontrada para exclusão.")
            return False