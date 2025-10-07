# Classes/Consultas.py - CÓDIGO FINAL E ESTÁVEL

from ArvoreBinaria.BaseDados import BaseDados
# Importações de módulo para uso interno (objetos serão injetados)
import Classes.Pacientes as pac_mod
import Classes.Medicos as med_mod
import Classes.Exames as exa_mod
import Classes.Diarias as dia_mod
import Classes.Especialidades as esp_mod
from datetime import datetime

class Consultas(BaseDados):
    """
    Gerencia a tabela Consultas, totalmente injetada com todas as dependências.
    Implementa a lógica de Relatórios (Item 6) e Ordenação (Item 7).
    """
    
    # CONSTRUTOR CORRIGIDO PARA INJEÇÃO DE DEPENDÊNCIA (DI)
    def __init__(self, pacientes_manager, medicos_manager, exames_manager, diarias_manager, especialidades_manager):
        super().__init__('Consultas')
        self.pacientes_manager = pacientes_manager
        self.medicos_manager = medicos_manager
        self.exames_manager = exames_manager
        self.diarias_manager = diarias_manager 
        self.especialidades_manager = especialidades_manager
        
    # --- FUNÇÕES AUXILIARES ---

    def _deserializar(self, registro_string):
        """Converte a string do disco em um dicionário básico."""
        try:
            campos = registro_string.split('|')
            return {
                "codigo": int(campos[0]), 
                "cod_paciente": int(campos[1]), 
                "cod_medico": int(campos[2]), 
                "cod_exame": int(campos[3]),
                "data": campos[4], # Data que pode vir com barras do arquivo
                "hora": campos[5], 
            }
        except Exception:
            return None

    def _realizar_lookups(self, consulta_data):
        """
        Realiza todos os lookups e cálculos necessários (JOIN).
        Lança ValueError se alguma dependência essencial não for encontrada.
        """
        
        # 1. Lookup de Médico, Especialidade e Limite Diário
        medico_completo = self.medicos_manager.consultar_medico(consulta_data["cod_medico"])
        
        if medico_completo:
            consulta_data["nome_medico"] = medico_completo["nome"]
            consulta_data["cod_especialidade"] = medico_completo["cod_especialidade"] 
            consulta_data["valor_consulta"] = medico_completo["valor_consulta"]
            consulta_data["limite_diario"] = medico_completo["limite_diario"]
            consulta_data["especialidade_desc"] = medico_completo.get("especialidade_desc", "N/A")
        else:
            raise ValueError(f"Médico {consulta_data['cod_medico']} não encontrado.")
        
        # 2. Lookup de Exame
        exame_completo = self.exames_manager.consultar_exame(consulta_data["cod_exame"])
        if exame_completo:
            consulta_data["desc_exame"] = exame_completo["descricao"]
            consulta_data["valor_exame"] = exame_completo["valor_exame"]
        else:
            raise ValueError(f"Exame {consulta_data['cod_exame']} não encontrado.")

        # 3. Lookup de Paciente e Cidade/IMC
        paciente_completo = self.pacientes_manager.consultar_paciente(consulta_data["cod_paciente"])
        if paciente_completo:
            consulta_data["nome_paciente"] = paciente_completo["nome"]
            consulta_data["nome_cidade_paciente"] = paciente_completo.get("cidade_nome", "N/A")
            consulta_data["imc"] = paciente_completo.get("imc", 0.0)
            consulta_data["diagnostico_imc"] = paciente_completo.get("diagnostico", "N/A")
        else:
            raise ValueError(f"Paciente {consulta_data['cod_paciente']} não encontrado.")
        
        # 4. Cálculo do Valor Total (Item 5.2)
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
        """Retorna a consulta enriquecida."""
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None: return None 
        
        consulta_data = self._deserializar(registro_string)
        if consulta_data is None: return None
        
        # CRÍTICO: Limpa a data do dado lido do arquivo antes de enriquecer
        data_raw = consulta_data.get('data', '')
        consulta_data['data'] = data_raw.replace('/', '').replace('-', '').replace(' ', '').strip()
        
        return self._realizar_lookups(consulta_data)

    def excluir_consulta(self, codigo):
        """Exclusão Lógica e atualização de Diárias (-1) (Item 5.4)."""
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

    # --- MÉTODOS DE RELATÓRIO (Item 6 e 7) ---

    def _obter_consultas_com_valor(self):
        """Lê todas as consultas ATIVAS e as enriquece. Útil para qualquer relatório."""
        registros_strings = self.ler_todos() 
        consultas_completas = []
        
        print(f"\n[DEBUG] Total de registros ATIVOS lidos do disco (Consulta): {len(registros_strings)}")
        
        for reg_str in registros_strings:
            consulta_data = self._deserializar(reg_str)
            if consulta_data:
                # CRÍTICO: Limpa a data do dado lido do arquivo para o formato AAAAMMDD
                data_raw = consulta_data.get('data', '')
                consulta_data['data'] = data_raw.replace('/', '').replace('-', '').replace(' ', '').strip()
                
                try:
                    consulta_completa = self._realizar_lookups(consulta_data)
                    print(f"[DEBUG] Sucesso JOIN Cód: {consulta_completa['codigo']} | Data: {consulta_completa['data']}")
                    consultas_completas.append(consulta_completa)
                except Exception as e:
                    print(f"[AVISO CRÍTICO] Falha no JOIN/Lookup da Consulta {consulta_data.get('codigo')}. Erro: {e}. O registro é ignorado no faturamento.")
                    
        return consultas_completas

    def faturamento_por_dia(self, data):
        """
        Item 6.1: Retorna a lista de consultas detalhadas do dia.
        CORRIGIDO: Retorna a LISTA filtrada.
        """
        consultas = self._obter_consultas_com_valor()
        
        # Filtra as consultas pela data (AAAAMMDD limpa)
        relatorio_filtrado = [cons for cons in consultas if cons.get('data') == data]
        
        return relatorio_filtrado

    def faturamento_por_periodo(self, data_inicial, data_final):
        """
        Item 6.2: Retorna a lista de consultas detalhadas do período.
        CORRIGIDO: Retorna a LISTA filtrada.
        """
        if data_inicial > data_final:
            data_inicial, data_final = data_final, data_inicial
            
        consultas = self._obter_consultas_com_valor()
        
        # Filtra as consultas pelo período de datas (AAAAMMDD limpas)
        relatorio_filtrado = [
            cons for cons in consultas 
            if data_inicial <= cons.get('data', '') <= data_final
        ]

        return relatorio_filtrado
        
    def faturamento_por_medico(self, cod_medico):
        """
        Item 6.3: Retorna a lista de consultas detalhadas do médico.
        CORRIGIDO: Retorna a LISTA filtrada.
        """
        consultas = self._obter_consultas_com_valor()
        relatorio_filtrado = [cons for cons in consultas if cons.get('cod_medico') == cod_medico]
        return relatorio_filtrado

    def faturamento_por_especialidade(self, cod_especialidade):
        """
        Item 6.4: Retorna a lista de consultas detalhadas da especialidade.
        CORRIGIDO: Retorna a LISTA filtrada.
        """
        consultas = self._obter_consultas_com_valor()
        relatorio_filtrado = [cons for cons in consultas if cons.get('cod_especialidade') == cod_especialidade]
        return relatorio_filtrado
    
    def relatorio_ordenado(self):
        """
        Item 7: Retorna a lista completa de consultas ordenadas por código (usando índice).
        """
        
        chaves_ordenadas = self.indice.percurso_em_ordem() 
        lista_consultas_ordenadas = []
        
        for codigo_consulta, endereco_byte in chaves_ordenadas:
            
            registro_string = self.gerenciador_arquivo.ler_registro_por_endereco(endereco_byte)
            if registro_string is None: continue 
            
            consulta_data = self._deserializar(registro_string)
            if consulta_data:
                # Limpa a data do dado lido do arquivo para o formato AAAAMMDD
                data_raw = consulta_data.get('data', '')
                consulta_data['data'] = data_raw.replace('/', '').replace('-', '').replace(' ', '').strip()

                try:
                    consulta_completa = self._realizar_lookups(consulta_data)
                    lista_consultas_ordenadas.append(consulta_completa)
                except Exception as e:
                    print(f"[AVISO CRÍTICO] Falha na Consulta {codigo_consulta} durante a ordenação. Erro: {e}")

        return lista_consultas_ordenadas