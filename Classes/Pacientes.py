

from ArvoreBinaria.BaseDados import BaseDados


class Pacientes(BaseDados):
   
    def __init__(self, cidades_manager): 
        super().__init__('Pacientes')
        self.cidades_manager = cidades_manager 

 
    
    def _calcular_imc(self, peso, altura):
        """Calcula o IMC e retorna o valor e o diagnóstico."""
        altura_m = altura / 100.0 if altura > 0 else 0
        if altura_m == 0:
            return 0, "Dados Inválidos"
            
        imc = peso / (altura_m ** 2)
        
        # Diagnóstico
        if imc < 18.5:
            diagnostico = "Abaixo do peso"
        elif 18.5 <= imc < 25:
            diagnostico = "Peso normal"
        elif 25 <= imc < 30:
            diagnostico = "Sobrepeso"
        else: # IMC >= 30
            diagnostico = "Obesidade"
            
        return round(imc, 2), diagnostico


    def _deserializar(self, registro_string):
      
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]), "nome": campos[1], "data_nascimento": campos[2], 
                "endereco": campos[3], "telefone": campos[4], "cod_cidade": int(campos[5]), 
                "peso": float(campos[6]), "altura": float(campos[7]), 
            }
        except Exception:
            return None

    
    def incluir_paciente(self, codigo, nome, dt_nasc, end, tel, cod_cidade, peso, altura):
       
        if not self.cidades_manager.buscar_por_chave(cod_cidade): 
            print(f"ERRO: Inclusão abortada. Código da Cidade {cod_cidade} não encontrado.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Paciente com código {codigo} já existe.")
            return False

        registro_formatado = f"{codigo}|{nome}|{dt_nasc}|{end}|{tel}|{cod_cidade}|{peso}|{altura}"
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Paciente {nome} ({codigo}) incluído.")
        return True

    def consultar_paciente(self, codigo):
        
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None 
        
        paciente_data = self._deserializar(registro_string)
        if paciente_data is None:
            return None

        
        cidade = self.cidades_manager.consultar_cidade(paciente_data["cod_cidade"])
        if cidade:
            paciente_data["cidade_nome"] = cidade["descricao"]
            paciente_data["cidade_estado"] = cidade["estado"]
        
        
        imc, diagnostico = self._calcular_imc(paciente_data["peso"], paciente_data["altura"])
        paciente_data["imc"] = imc
        paciente_data["diagnostico"] = diagnostico
        
        return paciente_data
    
    def listar_todos(self):
        registros_strings = self.ler_todos()
        pacientes_completos = []
        for reg_str in registros_strings:
            paciente_data = self._deserializar(reg_str)
            if paciente_data:
                imc, diagnostico = self._calcular_imc(paciente_data["peso"], paciente_data["altura"])
                paciente_data["imc"] = imc
                paciente_data["diagnostico"] = diagnostico
                
               
                cidade = self.cidades_manager.consultar_cidade(paciente_data["cod_cidade"])
                paciente_data["cidade_nome"] = cidade["descricao"] if cidade else "N/A"
                paciente_data["cidade_estado"] = cidade["estado"] if cidade else "N/A"
                
                pacientes_completos.append(paciente_data)
        return pacientes_completos

    def excluir_paciente(self, codigo):
        
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Paciente {codigo} marcado para exclusão.")
            return True
        else:
            print(f"ERRO: Paciente com código {codigo} não encontrado para exclusão.")
            return False