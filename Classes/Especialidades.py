

from ArvoreBinaria.BaseDados import BaseDados

class Especialidades(BaseDados):
    
    
    def __init__(self):
        super().__init__('Especialidades')

    def incluir_especialidade(self, codigo, descricao, valor_consulta, limite_diario):
        """Implementa Inclusão (1.1)."""
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Especialidade com código {codigo} já existe.")
            return False 

        # Salva o valor da consulta e limite diário
        registro_formatado = f"{codigo}|{descricao}|{valor_consulta}|{limite_diario}"
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Especialidade {descricao} ({codigo}) incluída.")
        return True
    
    def _deserializar(self, registro_string):
       
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]),
                "descricao": campos[1],
                # CRÍTICO: Conversão para float e int para cálculos
                "valor_consulta": float(campos[2]), 
                "limite_diario": int(campos[3]), 
            }
        except Exception:
            return None

    def consultar_especialidade(self, codigo):
        
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None
        return self._deserializar(registro_string)

    def listar_todas(self):
     
        registros_strings = self.ler_todos()
        especialidades_listadas = [
            self._deserializar(reg_str) 
            for reg_str in registros_strings 
            if self._deserializar(reg_str) is not None
        ]
        return especialidades_listadas

    def excluir_especialidade(self, codigo):
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Especialidade {codigo} marcada para exclusão.")
            return True
        else:
            print(f"ERRO: Especialidade com código {codigo} não encontrada para exclusão.")
            return False