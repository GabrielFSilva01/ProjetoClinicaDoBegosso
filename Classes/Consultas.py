

from ArvoreBinaria.BaseDados import BaseDados
# Manter as importações de módulo para tipagem/uso interno, mas os objetos serão INJETADOS
import Classes.Pacientes as pac_mod
import Classes.Medicos as med_mod
import Classes.Exames as exa_mod
import Classes.Diarias as dia_mod
import Classes.Especialidades as esp_mod
from datetime import datetime

class Consultas(BaseDados):
   
    
    
    def __init__(self, pacientes_manager, medicos_manager, exames_manager, diarias_manager, especialidades_manager):
        super().__init__('Consultas')
      
        self.pacientes_manager = pacientes_manager
        self.medicos_manager = medicos_manager
        self.exames_manager = exames_manager
        self.diarias_manager = diarias_manager 
        self.especialidades_manager = especialidades_manager
        
 

    def _deserializar(self, registro_string):
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]), 
                "cod_paciente": int(campos[1]), 
                "cod_medico": int(campos[2]), 
                "cod_exame": int(campos[3]),
                "data": campos[4], # Formato AAAAMMDD
                "hora": campos[5], 
            }
        except Exception:
            return None

    def _realizar_lookups(self, consulta_data):
        
        
       
        medico_completo = self.medicos_manager.consultar_medico(consulta_data["cod_medico"])
        
        if medico_completo:
            consulta_data["nome_medico"] = medico_completo["nome"]
            consulta_data["cod_especialidade"] = medico_completo["cod_especialidade"] 
            consulta_data["valor_consulta"] = medico_completo["valor_consulta"]
            consulta_data["limite_diario"] = medico_completo["limite_diario"]
            consulta_data["especialidade_desc"] = medico_completo.get("especialidade_desc", "N/A")
        else:
            consulta_data.update({"nome_medico": "N/A", "cod_especialidade": 0, "valor_consulta": 0.0, "limite_diario": 0, "especialidade_desc": "N/A"})
        
       
        exame_completo = self.exames_manager.consultar_exame(consulta_data["cod_exame"])
        if exame_completo:
            consulta_data["desc_exame"] = exame_completo["descricao"]
            consulta_data["valor_exame"] = exame_completo["valor_exame"]
        else:
            consulta_data.update({"desc_exame": "N/A", "valor_exame": 0.0})

        
        paciente_completo = self.pacientes_manager.consultar_paciente(consulta_data["cod_paciente"])
        if paciente_completo:
            consulta_data["nome_paciente"] = paciente_completo["nome"]
            consulta_data["nome_cidade_paciente"] = paciente_completo.get("cidade_nome", "N/A")
            consulta_data["imc"] = paciente_completo.get("imc", 0.0)
            consulta_data["diagnostico_imc"] = paciente_completo.get("diagnostico", "N/A")
        else:
            consulta_data.update({"nome_paciente": "N/A", "nome_cidade_paciente": "N/A", "imc": 0.0, "diagnostico_imc": "N/A"})
        
      
        v_total = consulta_data.get("valor_consulta", 0.0) + consulta_data.get("valor_exame", 0.0)
        consulta_data["valor_total_a_pagar"] = round(v_total, 2)
        
        return consulta_data

    # --- OPERAÇÕES CRUD (MANTIDAS) ---

    def incluir_consulta(self, codigo, cod_paciente, cod_medico, cod_exame, data, hora):
        """Implementa Inclusão (1.1). Verifica vagas (5.1) e atualiza Diárias (5.3)."""
        medico = self.medicos_manager.consultar_medico(cod_medico)
        if not medico:
            print("ERRO: Médico não encontrado.")
            return False
        
        cod_especialidade = medico.get("cod_especialidade")
        limite_diario = medico.get("limite_diario", 0)
        
        diaria = self.diarias_manager.consultar_diaria(data, cod_especialidade)
        vagas_ocupadas = diaria.get("quantidade", 0) 
        
        if vagas_ocupadas >= limite_diario:
            print(f"ERRO: Limite de consultas diárias ({limite_diario}) para esta especialidade/dia atingido.")
            return False
            
        if not all([self.pacientes_manager.buscar_por_chave(cod_paciente), 
                     self.exames_manager.buscar_por_chave(cod_exame)]):
            print("ERRO: Paciente ou Exame não encontrado. Inclusão abortada.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Consulta com código {codigo} já existe.")
            return False

        registro_formatado = f"{codigo}|{cod_paciente}|{cod_medico}|{cod_exame}|{data}|{hora}"
        self.incluir(registro_formatado, codigo)
        
        self.diarias_manager.atualizar_quantidade(data, cod_especialidade, 1)
        
        print(f"SUCESSO: Consulta {codigo} agendada. Vagas restantes: {limite_diario - (vagas_ocupadas + 1)}")
        return True

    def consultar_consulta(self, codigo):
       
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None: return None 
        
        consulta_data = self._deserializar(registro_string)
        if consulta_data is None: return None
        
        return self._realizar_lookups(consulta_data)

    def excluir_consulta(self, codigo):
        
        consulta = self.consultar_consulta(codigo)
        if consulta is None:
            print(f"ERRO: Consulta {codigo} não encontrada para exclusão.")
            return False

        if self.excluir_por_chave(codigo):
            cod_especialidade = consulta.get("cod_especialidade")
            data = consulta["data"]
            
            if cod_especialidade and self.diarias_manager.atualizar_quantidade(data, cod_especialidade, -1):
                print(f"SUCESSO: Consulta {codigo} excluída e vaga liberada no controle diário.")
                return True
            else:
                print(f"AVISO: Consulta {codigo} excluída, mas falha ao decrementar vaga no Diárias. Verifique a diária {data}/{cod_especialidade}.")
                return True
        else:
            return False

    

    def _obter_consultas_com_valor(self):
        
        registros_strings = self.ler_todos() 
        consultas_completas = []
        
        for reg_str in registros_strings:
            consulta_data = self._deserializar(reg_str)
            if consulta_data:
                try:
                    consulta_completa = self._realizar_lookups(consulta_data)
                    consultas_completas.append(consulta_completa)
                except Exception as e:
                    print(f"AVISO: Pulando registro com erro de lookup/dependência: {e}")
                    
        return consultas_completas

    def faturamento_por_dia(self, data):
   
        faturamento_total = 0.0
        consultas = self._obter_consultas_com_valor()
        
        print(f"\n--- Faturamento do Dia: {data} ---")
        
        for cons in consultas:
            if cons['data'] == data:
                faturamento_total += cons['valor_total_a_pagar']
                print(f"  Consulta {cons['codigo']} ({cons['nome_paciente']}): R$ {cons['valor_total_a_pagar']:.2f}")
                
        print(f"FATURAMENTO TOTAL DO DIA {data}: R$ {faturamento_total:.2f}")
        return faturamento_total

    def faturamento_por_periodo(self, data_inicial, data_final):
        
        faturamento_total = 0.0
        
        if data_inicial > data_final:
            data_inicial, data_final = data_final, data_inicial
            
        consultas = self._obter_consultas_com_valor()
        
        print(f"\n--- Faturamento do Período: {data_inicial} a {data_final} ---")
        
        for cons in consultas:
            data_consulta = cons['data']
            if data_inicial <= data_consulta <= data_final:
                faturamento_total += cons['valor_total_a_pagar']
                print(f"  Consulta {cons['codigo']} ({data_consulta} - {cons['nome_paciente']}): R$ {cons['valor_total_a_pagar']:.2f}")

        print(f"FATURAMENTO TOTAL NO PERÍODO: R$ {faturamento_total:.2f}")
        return faturamento_total
        
    def faturamento_por_medico(self, cod_medico):
        faturamento_total = 0.0
        
        medico_info = self.medicos_manager.consultar_medico(cod_medico)
        nome_medico = medico_info["nome"] if medico_info else f"Médico {cod_medico} (Não Encontrado)"
        
        consultas = self._obter_consultas_com_valor()
        
        print(f"\n--- Faturamento do(a) {nome_medico} ---")
        
        for cons in consultas:
            if cons['cod_medico'] == cod_medico:
                faturamento_total += cons['valor_total_a_pagar']
                print(f"  Consulta {cons['codigo']} ({cons['data']} - {cons['nome_paciente']}): R$ {cons['valor_total_a_pagar']:.2f}")

        print(f"FATURAMENTO TOTAL DO(A) {nome_medico}: R$ {faturamento_total:.2f}")
        return faturamento_total

    def faturamento_por_especialidade(self, cod_especialidade):
     
        faturamento_total = 0.0
        
        esp_info = self.especialidades_manager.consultar_especialidade(cod_especialidade)
        nome_especialidade = esp_info["descricao"] if esp_info else f"Especialidade {cod_especialidade} (Não Encontrada)"
        
        consultas = self._obter_consultas_com_valor()
        
        print(f"\n--- Faturamento da Especialidade: {nome_especialidade} ---")
        
        for cons in consultas:
            if cons.get('cod_especialidade') == cod_especialidade:
                faturamento_total += cons['valor_total_a_pagar']
                print(f"  Consulta {cons['codigo']} ({cons['data']} - {cons['nome_medico']}): R$ {cons['valor_total_a_pagar']:.2f}")

        print(f"FATURAMENTO TOTAL DA ESPECIALIDADE {nome_especialidade}: R$ {faturamento_total:.2f}")
        return faturamento_total
    
    def relatorio_ordenado(self):
       
        
        chaves_ordenadas = self.indice.percurso_em_ordem() 
        lista_consultas_ordenadas = []
        
        for codigo_consulta, endereco_byte in chaves_ordenadas:
            
            registro_string = self.gerenciador_arquivo.ler_registro_por_endereco(endereco_byte)
            if registro_string is None: continue 
            
            consulta_data = self._deserializar(registro_string)
            if consulta_data:
                try:
                    consulta_completa = self._realizar_lookups(consulta_data)
                    lista_consultas_ordenadas.append(consulta_completa)
                except Exception as e:
                    print(f"AVISO: Pulando registro {codigo_consulta} com erro durante o enriquecimento: {e}")
        
        valor_total_pago = sum(c['valor_total_a_pagar'] for c in lista_consultas_ordenadas)
        pacientes_unicos = set(c['cod_paciente'] for c in lista_consultas_ordenadas)
        
        print("\n--- RELATÓRIO DE CONSULTAS ORDENADO POR CÓDIGO (Item 7) ---")
        for cons in lista_consultas_ordenadas:
            print(f"Cód. Consulta: {cons['codigo']} | Paciente: {cons['nome_paciente']} | Médico: {cons['nome_medico']}")
            print(f"  > Valor a Pagar: R$ {cons['valor_total_a_pagar']:.2f}")
            
        print("------------------------------------------------------------------")
        print(f"QUANTIDADE TOTAL DE REGISTROS DE CONSULTAS: {len(lista_consultas_ordenadas)}")
        print(f"QUANTIDADE TOTAL DE PACIENTES ATENDIDOS: {len(pacientes_unicos)}")
        print(f"VALOR TOTAL GERAL A SER PAGO: R$ {valor_total_pago:.2f}")
        
        return lista_consultas_ordenadas