

from ArvoreBinaria.BaseDados import BaseDados


class Exames(BaseDados):
  
    
    def __init__(self, especialidades_manager):
        super().__init__('Exames')
        
        self.especialidades_manager = especialidades_manager 

    

    def _deserializar(self, registro_string):
        
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
    
   

    def incluir_exame(self, codigo, descricao, cod_especialidade, valor_exame):
        
        
        
        if not self.especialidades_manager.buscar_por_chave(cod_especialidade):
            print(f"ERRO: Inclusão abortada. Código da Especialidade {cod_especialidade} não encontrado.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Exame com código {codigo} já existe.")
            return False

        
        registro_formatado = f"{codigo}|{descricao}|{cod_especialidade}|{valor_exame}"
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Exame '{descricao}' ({codigo}) incluído.")
        return True

    def consultar_exame(self, codigo):
        
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None 
        
        exame_data = self._deserializar(registro_string)
        if exame_data is None:
            return None
        
        
        especialidade = self.especialidades_manager.consultar_especialidade(exame_data["cod_especialidade"])
        if especialidade:
            exame_data["especialidade_desc"] = especialidade["descricao"]
        else:
            exame_data["especialidade_desc"] = "N/A"
            
        return exame_data
    
    def listar_todos(self):
     
        registros_strings = self.ler_todos()
        exames_completos = []
        
        for reg_str in registros_strings:
            exame_data = self._deserializar(reg_str)
            if exame_data:
              
                especialidade = self.especialidades_manager.consultar_especialidade(exame_data["cod_especialidade"])
                exame_data["especialidade_desc"] = especialidade["descricao"] if especialidade else "N/A"
                
                exames_completos.append(exame_data)
        return exames_completos

    def excluir_exame(self, codigo):
        
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Exame {codigo} marcado para exclusão.")
            return True
        else:
            print(f"ERRO: Exame com código {codigo} não encontrado para exclusão.")
            return False