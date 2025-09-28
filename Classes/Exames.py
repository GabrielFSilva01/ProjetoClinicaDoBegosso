# exames.py

from ArvoreBinaria.BaseDados import BaseDados
from Classes.Especialidades import Especialidades 

class Exames(BaseDados):
    """
    Gerencia a tabela Exames.
    Faz lookup na tabela Especialidades para obter o nome da especialidade (Item 4).
    Estrutura: Cod_Exame|Descricao|Cod_Especialidade|Valor_Exame
    """
    
    def __init__(self):
        super().__init__('Exames')
        # Cria uma instância do gerenciador de Especialidades para os lookups
        self.especialidades_manager = Especialidades()

    # --- FUNÇÕES AUXILIARES ---

    def _deserializar(self, registro_string):
        """Converte a string do disco em um dicionário básico."""
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]),
                "descricao": campos[1],
                "cod_especialidade": int(campos[2]),
                "valor_exame": float(campos[3]),
            }
        except Exception:
            return None
    
    # --- OPERAÇÕES CRUD COM LÓGICA ---

    def incluir_exame(self, codigo, descricao, cod_especialidade, valor_exame):
        """Implementa Inclusão (1.1), validando a Especialidade."""
        
        # 1. Validação de Relacionamento (Item 4)
        if not self.especialidades_manager.buscar_por_chave(cod_especialidade):
            print(f"ERRO: Inclusão abortada. Código da Especialidade {cod_especialidade} não encontrado.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Exame com código {codigo} já existe.")
            return False

        # 2. Persistência
        registro_formatado = f"{codigo}|{descricao}|{cod_especialidade}|{valor_exame}"
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Exame '{descricao}' ({codigo}) incluído.")
        return True

    def consultar_exame(self, codigo):
        """
        Implementa Consulta (1.2). Realiza lookup na Especialidade (Item 4).
        """
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None 
        
        exame_data = self._deserializar(registro_string)
        if exame_data is None:
            return None
        
        # Item 4: Lookup na tabela Especialidades
        especialidade = self.especialidades_manager.consultar_especialidade(exame_data["cod_especialidade"])
        if especialidade:
            exame_data["especialidade_desc"] = especialidade["descricao"]
        else:
            exame_data["especialidade_desc"] = "N/A"
            
        return exame_data
    
    def listar_todos(self):
        """Implementa Leitura Exaustiva (1.4). Retorna a lista completa com lookups."""
        registros_strings = self.ler_todos()
        exames_completos = []
        
        for reg_str in registros_strings:
            exame_data = self._deserializar(reg_str)
            if exame_data:
                # Reutiliza a lógica de lookup da consulta para cada item
                especialidade = self.especialidades_manager.consultar_especialidade(exame_data["cod_especialidade"])
                exame_data["especialidade_desc"] = especialidade["descricao"] if especialidade else "N/A"
                
                exames_completos.append(exame_data)
        return exames_completos

    def excluir_exame(self, codigo):
        """Implementa Exclusão (1.3) (Exclusão Lógica e remoção do índice)."""
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Exame {codigo} marcado para exclusão.")
            return True
        else:
            print(f"ERRO: Exame com código {codigo} não encontrado para exclusão.")
            return False