# consultas.py - CÓDIGO FINAL E CORRIGIDO

# --- IMPORTAÇÕES ROBUSTAS (Corrigindo "Module is not callable") ---
from ArvoreBinaria.BaseDados import BaseDados
import  Classes.Pacientes as pac_mod
import Classes.Medicos as med_mod
import Classes.Exames as exa_mod
import Classes.Diarias as dia_mod
import  Classes.Especialidades as esp_mod
from datetime import datetime

class Consultas(BaseDados):
    """
    Gerencia a tabela Consultas, integrando todas as regras de negócio (Itens 5, 6, 7).
    Estrutura: Cod_Cons|Cod_Pac|Cod_Med|Cod_Exame|Data|Hora
    """
    
    def __init__(self):
        super().__init__('Consultas')
        # Inicializa todos os managers chamando MÓDULO.CLASSE()
        self.pacientes_manager = pac_mod.Pacientes()
        self.medicos_manager = med_mod.Medicos()
        self.exames_manager = exa_mod.Exames()
        self.diarias_manager = dia_mod.Diarias() 
        self.especialidades_manager = esp_mod.Especialidades() 

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
                "data": campos[4], # Formato AAAAMMDD
                "hora": campos[5], 
            }
        except Exception:
            return None

    def _realizar_lookups(self, consulta_data):
        """Realiza todos os lookups e cálculos necessários (Item 5 e 5.2)."""
        
        # 1. Lookup de Médico, Especialidade e Limite Diário
        medico = self.medicos_manager.consultar_medico(consulta_data["cod_medico"])
        if medico:
            consulta_data["nome_medico"] = medico["nome"]
            consulta_data["cod_especialidade"] = medico["cod_especialidade"] 
            consulta_data["valor_consulta"] = medico["valor_consulta"]
            consulta_data["limite_diario"] = medico["limite_diario"]
        else:
            consulta_data.update({"nome_medico": "N/A", "cod_especialidade": 0, "valor_consulta": 0.0, "limite_diario": 0})
        
        # 2. Lookup de Exame
        exame = self.exames_manager.consultar_exame(consulta_data["cod_exame"])
        if exame:
            consulta_data["desc_exame"] = exame["descricao"]
            consulta_data["valor_exame"] = exame["valor_exame"]
        else:
            consulta_data.update({"desc_exame": "N/A", "valor_exame": 0.0})

        # 3. Lookup de Paciente e Cidade (Item 5)
        paciente = self.pacientes_manager.consultar_paciente(consulta_data["cod_paciente"])
        if paciente:
            consulta_data["nome_paciente"] = paciente["nome"]
            consulta_data["nome_cidade_paciente"] = paciente.get("cidade_nome", "N/A")
        else:
            consulta_data.update({"nome_paciente": "N/A", "nome_cidade_paciente": "N/A"})
        
        # 4. Cálculo do Valor Total (Item 5.2)
        v_total = consulta_data.get("valor_consulta", 0.0) + consulta_data.get("valor_exame", 0.0)
        consulta_data["valor_total_a_pagar"] = round(v_total, 2)
        
        return consulta_data

    # --- OPERAÇÕES CRUD COM REGRAS (Item 5) ---

    def incluir_consulta(self, codigo, cod_paciente, cod_medico, cod_exame, data, hora):
        """
        Implementa Inclusão (1.1). Verifica vagas (5.1) e atualiza Diárias (5.3).
        """
        # 1. Obter dados de Limite e Especialidade
        medico = self.medicos_manager.consultar_medico(cod_medico)
        if not medico:
            print("ERRO: Médico não encontrado.")
            return False
        
        cod_especialidade = medico.get("cod_especialidade")
        limite_diario = medico.get("limite_diario", 0)
        
        # 2. Item 5.1: Verificar Limite Diário (Vagas)
        diaria = self.diarias_manager.consultar_diaria(data, cod_especialidade)
        vagas_ocupadas = diaria["quantidade"]
        
        if vagas_ocupadas >= limite_diario:
            print(f"ERRO: Limite de consultas diárias ({limite_diario}) para esta especialidade/dia atingido.")
            return False
            
        # 3. Validação de chaves de Referência
        if not all([self.pacientes_manager.buscar_por_chave(cod_paciente), 
                    self.exames_manager.buscar_por_chave(cod_exame)]):
            print("ERRO: Paciente ou Exame não encontrado. Inclusão abortada.")
            return False
        if self.buscar_por_chave(codigo) is not None:
            print(f"ERRO: Consulta com código {codigo} já existe.")
            return False

        # 4. Persistência
        registro_formatado = f"{codigo}|{cod_paciente}|{cod_medico}|{cod_exame}|{data}|{hora}"
        self.incluir(registro_formatado, codigo)
        
        # 5. Item 5.3: Atualizar Tabela Diárias (+1)
        self.diarias_manager.atualizar_quantidade(data, cod_especialidade, 1)
        
        print(f"SUCESSO: Consulta {codigo} agendada. Vagas restantes: {limite_diario - (vagas_ocupadas + 1)}")
        return True

    def consultar_consulta(self, codigo):
        """
        Implementa Consulta (1.2). Realiza todos os lookups e cálculos (Item 5 e 5.2).
        """
        registro_string = self.buscar_por_chave(codigo)
        if registro_string is None:
            return None 
        
        consulta_data = self._deserializar(registro_string)
        if consulta_data is None:
            return None
        
        return self._realizar_lookups(consulta_data)

    def excluir_consulta(self, codigo):
        """
        Implementa Exclusão (1.3). Atualiza Tabela Diárias (-1) (Item 5.4).
        """
        consulta = self.consultar_consulta(codigo)
        if consulta is None:
            print(f"ERRO: Consulta {codigo} não encontrada para exclusão.")
            return False

        # 1. Exclusão Lógica e do Índice
        if self.excluir_por_chave(codigo):
            
            # 2. Item 5.4: Subtrair 1 na Quantidade de Consultas na tabela Diárias
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

    # --- MÉTODOS DE RELATÓRIO (Item 6 e 7) - A SEREM IMPLEMENTADOS ---
    pass

# consultas.py (continuação)

# ... (Os métodos CRUD da classe Consultas continuam acima)

    # --- IMPLEMENTAÇÃO DOS RELATÓRIOS (Item 6) ---

    def _obter_consultas_com_valor(self):
        """
        Lê todas as consultas, realiza lookups e retorna uma lista de dicionários completa.
        Utiliza a leitura exaustiva (self.ler_todos).
        """
        registros_strings = self.ler_todos()
        consultas_completas = []
        
        for reg_str in registros_strings:
            consulta_data = self._deserializar(reg_str)
            if consulta_data:
                # Realiza lookups e calcula o valor total (Item 5.2)
                consulta_completa = self._realizar_lookups(consulta_data)
                consultas_completas.append(consulta_completa)
                
        return consultas_completas

    def faturamento_por_dia(self, data):
        """Item 6.1: Exibir faturamento por dia (AAAAMMDD)."""
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
        """Item 6.2: Exibir faturamento por período (Data Inicial e Data Final - AAAAMMDD)."""
        faturamento_total = 0.0
        
        # Converte as datas para objetos date ou simplesmente usa comparação de strings (AAAAMMDD)
        if data_inicial > data_final:
            data_inicial, data_final = data_final, data_inicial # Garante a ordem
            
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
        """Item 6.3: Exibir faturamento por Médico."""
        faturamento_total = 0.0
        
        # OBTENDO NOME DO MÉDICO PARA O RELATÓRIO
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
        """Item 6.4: Exibir faturamento por Especialidade."""
        faturamento_total = 0.0
        
        # OBTENDO NOME DA ESPECIALIDADE PARA O RELATÓRIO
        esp_info = self.especialidades_manager.consultar_especialidade(cod_especialidade)
        nome_especialidade = esp_info["descricao"] if esp_info else f"Especialidade {cod_especialidade} (Não Encontrada)"
        
        consultas = self._obter_consultas_com_valor()
        
        print(f"\n--- Faturamento da Especialidade: {nome_especialidade} ---")
        
        for cons in consultas:
            # O lookup de médico já insere o 'cod_especialidade' na consulta
            if cons.get('cod_especialidade') == cod_especialidade:
                faturamento_total += cons['valor_total_a_pagar']
                print(f"  Consulta {cons['codigo']} ({cons['data']} - {cons['nome_medico']}): R$ {cons['valor_total_a_pagar']:.2f}")

        print(f"FATURAMENTO TOTAL DA ESPECIALIDADE {nome_especialidade}: R$ {faturamento_total:.2f}")
        return faturamento_total
    
    # consultas.py (Adição do Item 7)

# ... (Os métodos CRUD e Faturamento continuam acima)

    def relatorio_ordenado(self):
        """
        Item 7: Lê todas as consultas em ordem crescente de Código da Consulta.
        Exibe dados detalhados e totaliza o valor e a quantidade de pacientes.
        """
        # 1. OBTER CHAVES ORDENADAS DA ÁRVORE (O coração do item 7)
        # O percurso em-ordem da Árvore Binária garante a ordenação.
        chaves_ordenadas = self.indice.percurso_em_ordem() # Retorna [(chave, endereco), ...]
        
        total_pacientes = 0
        valor_total_pago = 0.0
        
        print("\n--- RELATÓRIO DE CONSULTAS ORDENADO POR CÓDIGO ---")
        print("------------------------------------------------------------------")
        
        # Lista para rastrear pacientes únicos, caso necessário (se o item 7 pedir
        # a contagem de pacientes que *têm* consulta, e não de consultas em si).
        pacientes_unicos = set() 

        # 2. ITERAR SOBRE A ORDEM E REALIZAR LOOKUPS DETALHADOS
        for codigo_consulta, endereco_byte in chaves_ordenadas:
            
            # Consulta o registro completo usando a chave ordenada
            consulta_completa = self.consultar_consulta(codigo_consulta)
            
            if consulta_completa:
                # 3. EXIBIR DETALHES
                
                # Coleta dados para totalização
                pacientes_unicos.add(consulta_completa['cod_paciente'])
                valor_total_pago += consulta_completa['valor_total_a_pagar']
                
                # Exibição dos dados solicitados
                print(f"Cód. Consulta: {consulta_completa['codigo']}")
                print(f"  Paciente: {consulta_completa['nome_paciente']} (Cód: {consulta_completa['cod_paciente']})")
                print(f"  Cidade do Pac.: {consulta_completa['nome_cidade_paciente']}")
                print(f"  Médico: {consulta_completa['nome_medico']}")
                print(f"  Exame: {consulta_completa['desc_exame']}")
                print(f"  Valor a Pagar: R$ {consulta_completa['valor_total_a_pagar']:.2f}")
                print("---")
        
        # 4. EXIBIR TOTALIZAÇÃO
        print("------------------------------------------------------------------")
        # Se for para contar o NÚMERO DE REGISTROS de consultas, use len(chaves_ordenadas).
        # Se for para contar quantos PACIENTES DIFERENTES foram atendidos, use len(pacientes_unicos).
        print(f"QUANTIDADE TOTAL DE REGISTROS DE CONSULTAS: {len(chaves_ordenadas)}")
        print(f"QUANTIDADE TOTAL DE PACIENTES ATENDIDOS: {len(pacientes_unicos)}")
        print(f"VALOR TOTAL GERAL A SER PAGO: R$ {valor_total_pago:.2f}")
        
        return valor_total_pago