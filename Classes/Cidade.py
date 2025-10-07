# Classes/Cidades.py - CÓDIGO FINAL

from ArvoreBinaria.BaseDados import BaseDados

class Cidades(BaseDados):
   
    
    def __init__(self):
       
        super().__init__('Cidades')

    def incluir_cidade(self, codigo, descricao, estado):
      
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Cidade com código {codigo} já existe.")
            return False 

        
        registro_formatado = f"{codigo}|{descricao}|{estado}"
        
        
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Cidade {descricao} ({codigo}) incluída.")
        return True
    
    def _deserializar(self, registro_string):
       
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]),
                "descricao": campos[1],
                "estado": campos[2],
            }
        except Exception:
            return None

    def consultar_cidade(self, codigo):
       
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None
        return self._deserializar(registro_string)

    def listar_todas(self):
        
        registros_strings = self.ler_todos()
        cidades_listadas = [
            self._deserializar(reg_str) 
            for reg_str in registros_strings 
            if self._deserializar(reg_str) is not None
        ]
        return cidades_listadas

    def excluir_cidade(self, codigo):
        
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Cidade {codigo} marcada para exclusão.")
            return True
        else:
            print(f"ERRO: Cidade com código {codigo} não encontrada para exclusão.")
            return False