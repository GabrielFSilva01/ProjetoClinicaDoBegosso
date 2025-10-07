

from ArvoreBinaria.BaseDados import BaseDados


class Medicos(BaseDados):
  
    
   
    def __init__(self, cidades_manager, especialidades_manager):
        super().__init__('Medicos')
        
        self.cidades_manager = cidades_manager 
        self.especialidades_manager = especialidades_manager


    def _deserializar(self, registro_string):
      
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]), "nome": campos[1], "endereco": campos[2], 
                "telefone": campos[3], "cod_cidade": int(campos[4]), "cod_especialidade": int(campos[5]),
            }
        except Exception:
            return None


    def incluir_medico(self, codigo, nome, end, tel, cod_cidade, cod_especialidade):
        
        
        
        if not self.cidades_manager.buscar_por_chave(cod_cidade):
            print(f"ERRO: Inclusão abortada. Cidade {cod_cidade} não encontrada.")
            return False
        if not self.especialidades_manager.buscar_por_chave(cod_especialidade):
            print(f"ERRO: Inclusão abortada. Especialidade {cod_especialidade} não encontrada.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Médico com código {codigo} já existe.")
            return False

        registro_formatado = f"{codigo}|{nome}|{end}|{tel}|{cod_cidade}|{cod_especialidade}"
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Médico {nome} ({codigo}) incluído.")
        return True

    def consultar_medico(self, codigo):
        
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None 
        
        medico_data = self._deserializar(registro_string)
        if medico_data is None:
            return None
        
  
        cidade = self.cidades_manager.consultar_cidade(medico_data["cod_cidade"])
        if cidade:
            medico_data["cidade_nome"] = cidade["descricao"]
            medico_data["cidade_estado"] = cidade["estado"]
        else:
            medico_data["cidade_nome"] = "N/A"
            medico_data["cidade_estado"] = "N/A"

        
        especialidade = self.especialidades_manager.consultar_especialidade(medico_data["cod_especialidade"])
        if especialidade:
            medico_data["especialidade_desc"] = especialidade["descricao"]
            medico_data["valor_consulta"] = especialidade["valor_consulta"]
            medico_data["limite_diario"] = especialidade["limite_diario"]
        else:
            medico_data["especialidade_desc"] = "N/A"
            medico_data["valor_consulta"] = 0.0
            medico_data["limite_diario"] = 0
            
        return medico_data
    
    def listar_todos(self):

        registros_strings = self.ler_todos()
        medicos_completos = []
        
        for reg_str in registros_strings:
            medico_data = self._deserializar(reg_str)
            if medico_data:
                cidade = self.cidades_manager.consultar_cidade(medico_data["cod_cidade"])
                medico_data["cidade_nome"] = cidade["descricao"] if cidade else "N/A"
                medico_data["cidade_estado"] = cidade["estado"] if cidade else "N/A"
                
                especialidade = self.especialidades_manager.consultar_especialidade(medico_data["cod_especialidade"])
                medico_data["especialidade_desc"] = especialidade["descricao"] if especialidade else "N/A"
                medico_data["valor_consulta"] = especialidade["valor_consulta"] if especialidade else 0.0
                medico_data["limite_diario"] = especialidade["limite_diario"] if especialidade else 0
                
                medicos_completos.append(medico_data)
        return medicos_completos

    def excluir_medico(self, codigo):
        
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Médico {codigo} marcado para exclusão.")
            return True
        else:
            print(f"ERRO: Médico com código {codigo} não encontrado para exclusão.")
            return False