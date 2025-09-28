# pacientes.py

from ArvoreBinaria.BaseDados import BaseDados
from Classes.Cidade import Cidades # Dependência: Cidades

class Pacientes(BaseDados):
    """
    Gerencia a tabela Pacientes.
    Inclui relacionamento com Cidades (Item 2) e cálculo do IMC (Item 2.1).
    Estrutura: Cod_Pac|Nome|Dt_Nasc|Endereco|Telefone|Cod_Cidade|Peso|Altura
    """
    def __init__(self):
        super().__init__('Pacientes')
        # Cria uma instância do gerenciador de Cidades para os lookups
        self.cidades_manager = Cidades()

    # --- LÓGICA DE NEGÓCIOS (Item 2.1) ---
    
    def _calcular_imc(self, peso, altura):
        """Calcula o IMC e retorna o valor e o diagnóstico."""
        # Altura está em cm, converte para metros
        altura_m = altura / 100.0 if altura > 0 else 0
        if altura_m == 0:
            return 0, "Dados Inválidos"
            
        # Fórmula: IMC = Peso (kg) / Altura (m)^2
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

    # --- FUNÇÕES AUXILIARES ---

    def _deserializar(self, registro_string):
        """Converte a string do disco em um dicionário básico."""
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]), "nome": campos[1], "data_nascimento": campos[2], 
                "endereco": campos[3], "telefone": campos[4], "cod_cidade": int(campos[5]), 
                "peso": float(campos[6]), "altura": float(campos[7]), 
            }
        except Exception:
            return None

    # --- OPERAÇÕES CRUD COM LÓGICA ---
    
    def incluir_paciente(self, codigo, nome, dt_nasc, end, tel, cod_cidade, peso, altura):
        """Implementa Inclusão (1.1), validando Cod_Cidade."""
        # 1. Validação de Relacionamento
        if not self.cidades_manager.buscar_por_chave(cod_cidade):
            print(f"ERRO: Inclusão abortada. Código da Cidade {cod_cidade} não encontrado.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Paciente com código {codigo} já existe.")
            return False

        # 2. Persistência
        registro_formatado = f"{codigo}|{nome}|{dt_nasc}|{end}|{tel}|{cod_cidade}|{peso}|{altura}"
        self.incluir(registro_formatado, codigo)
        print(f"SUCESSO: Paciente {nome} ({codigo}) incluído.")
        return True

    def consultar_paciente(self, codigo):
        """
        Implementa Consulta (1.2). Realiza lookup de Cidade (2) e calcula IMC (2.1).
        """
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None 
        
        paciente_data = self._deserializar(registro_string)
        if paciente_data is None:
            return None

        # Item 2: Lookup na Cidades
        cidade = self.cidades_manager.consultar_cidade(paciente_data["cod_cidade"])
        if cidade:
            paciente_data["cidade_nome"] = cidade["descricao"]
            paciente_data["cidade_estado"] = cidade["estado"]
        
        # Item 2.1: Cálculo do IMC
        imc, diagnostico = self._calcular_imc(paciente_data["peso"], paciente_data["altura"])
        paciente_data["imc"] = imc
        paciente_data["diagnostico"] = diagnostico
            
        return paciente_data
    
    def listar_todos(self):
        """Implementa Leitura Exaustiva (1.4). Retorna a lista completa com lookups e IMC."""
        registros_strings = self.ler_todos()
        pacientes_completos = []
        for reg_str in registros_strings:
            paciente_data = self._deserializar(reg_str)
            if paciente_data:
                # Reutiliza a lógica da consulta para incluir IMC e Cidade em cada item
                imc, diagnostico = self._calcular_imc(paciente_data["peso"], paciente_data["altura"])
                paciente_data["imc"] = imc
                paciente_data["diagnostico"] = diagnostico
                
                cidade = self.cidades_manager.consultar_cidade(paciente_data["cod_cidade"])
                paciente_data["cidade_nome"] = cidade["descricao"] if cidade else "N/A"
                paciente_data["cidade_estado"] = cidade["estado"] if cidade else "N/A"
                
                pacientes_completos.append(paciente_data)
        return pacientes_completos

    def excluir_paciente(self, codigo):
        """Implementa Exclusão (1.3) (Exclusão Lógica e remoção do índice)."""
        if self.excluir_por_chave(codigo):
            print(f"SUCESSO: Paciente {codigo} marcado para exclusão.")
            return True
        else:
            print(f"ERRO: Paciente com código {codigo} não encontrado para exclusão.")
            return False