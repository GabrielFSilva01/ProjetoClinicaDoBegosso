

from ArvoreBinaria.BaseDados import BaseDados

class Diarias(BaseDados):
  
    
    def __init__(self):
        super().__init__('Diarias')

    def _gerar_chave_diaria(self, data, cod_especialidade):
 
        return f"{data}-{cod_especialidade}"

    def _deserializar(self, registro_string):
     
        try:
         
            chave, quantidade = registro_string.split('|')
            return {
                "chave": chave, 
                "quantidade": int(quantidade) 
            }
        except Exception:
            return None

    def consultar_diaria(self, data, cod_especialidade):
        
        chave = self._gerar_chave_diaria(data, cod_especialidade)
        registro_string = self.buscar_por_chave(chave)
        
        if registro_string is None:
           
            return {"chave": chave, "quantidade": 0} 
            
        return self._deserializar(registro_string)

    def atualizar_quantidade(self, data, cod_especialidade, delta):
        
        chave = self._gerar_chave_diaria(data, cod_especialidade)
        diaria_atual = self.consultar_diaria(data, cod_especialidade)
        
        nova_quantidade = diaria_atual["quantidade"] + delta
        
        if nova_quantidade < 0:
            print("AVISO: Tentativa de decrementar a quantidade de consultas para um valor negativo. Corrigido para 0.")
            nova_quantidade = 0 
            
        registro_formatado = f"{chave}|{nova_quantidade}"
        
        try:
            
            self.incluir(registro_formatado, chave)
            return True
        except Exception as e:
            print(f"Erro ao atualizar diária {chave}: {e}")
            return False

    

    def listar_todas(self):
        
        registros_strings = self.ler_todos()
        diarias_listadas = [
            self._deserializar(reg_str) 
            for reg_str in registros_strings 
            if self._deserializar(reg_str) is not None
        ]
        return diarias_listadas

    def excluir_diaria(self, data, cod_especialidade):
        
        chave = self._gerar_chave_diaria(data, cod_especialidade)
        
        if self.excluir_por_chave(chave):
            print(f"SUCESSO: Diária {chave} marcada para exclusão.")
            return True
        else:
            print(f"AVISO: Diária com chave {chave} não encontrada para exclusão.")
            return False