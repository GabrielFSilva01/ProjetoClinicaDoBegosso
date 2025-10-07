import customtkinter as ctk
from tkinter import messagebox, simpledialog 
from datetime import datetime

# Importações dos módulos (DAOs)
import Classes.Cidade as cid_mod
import Classes.Especialidades as esp_mod
import Classes.Pacientes as pac_mod
import Classes.Medicos as med_mod
import Classes.Exames as exa_mod
import Classes.Consultas as con_mod 
import Classes.Diarias as dia_mod 

class ClinicaApp(ctk.CTk):
    """Classe principal da aplicação com interface gráfica (GUI)."""
    
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Clínica - Arquivos Indexados")
        self.geometry("900x650") 

        # --- CRIAÇÃO CENTRALIZADA DE INSTÂNCIAS (INJEÇÃO DE DEPENDÊNCIA) ---
        
        # 1. Classes Raiz
        self.cidades_db = cid_mod.Cidades()
        self.especialidades_db = esp_mod.Especialidades()
        self.diarias_db = dia_mod.Diarias() 

        # 2. Classes Dependentes (Resolvendo a ordem de dependência)
        
        self.pacientes_db = pac_mod.Pacientes(cidades_manager=self.cidades_db)
        self.exames_db = exa_mod.Exames(especialidades_manager=self.especialidades_db)
        self.medicos_db = med_mod.Medicos(
            cidades_manager=self.cidades_db,
            especialidades_manager=self.especialidades_db
        )
        
        # Consultas (Depende de TODOS)
        self.consultas_db = con_mod.Consultas(
            pacientes_manager=self.pacientes_db,
            medicos_manager=self.medicos_db,
            exames_manager=self.exames_db,
            diarias_manager=self.diarias_db,
            especialidades_manager=self.especialidades_db
        )

        # --- Criação do Notebook (Abas) ---
        self.notebook = ctk.CTkTabview(self, width=880, height=580)
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)

        self.notebook.add("Cadastro Manual")
        self.notebook.add("Consultas & Relatórios")
        
        # Chamadas de setup
        self._setup_cadastro_tab() 
        self._setup_relatorios_tab()

   
    def _setup_cadastro_tab(self):
        """Configura a interface de inclusão de dados."""
        frame = self.notebook.tab("Cadastro Manual")
        
        self.cadastro_frame = ctk.CTkFrame(frame)
        self.cadastro_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.cadastro_frame, text="Selecione a Tabela para Cadastro:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        entidades = ["Cidades", "Especialidades", "Pacientes", "Médicos", "Exames", "Consultas"]
        self.entidade_var = ctk.StringVar(value=entidades[0])
        self.entidade_menu = ctk.CTkOptionMenu(self.cadastro_frame, values=entidades, 
                                                command=self._carregar_formulario,
                                                variable=self.entidade_var)
        self.entidade_menu.pack(pady=10)

        self.form_container = ctk.CTkFrame(self.cadastro_frame, corner_radius=10, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._carregar_formulario(self.entidade_var.get())

    def _carregar_formulario(self, escolha):
        """Limpa o container e carrega o formulário específico."""
        for widget in self.form_container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.form_container, text=f"Formulário de Cadastro: {escolha}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        if escolha == "Cidades": self._criar_form_cidades()
        elif escolha == "Especialidades": self._criar_form_especialidades()
        elif escolha == "Pacientes": self._criar_form_pacientes()
        elif escolha == "Médicos": self._criar_form_medicos()
        elif escolha == "Exames": self._criar_form_exames()
        elif escolha == "Consultas": self._criar_form_consultas()
        
    def _criar_form_cidades(self):
        """Cria os campos para a entidade Cidades."""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10) 
        form_sub_frame.grid_columnconfigure(1, weight=1) 

        fields = ["Código da Cidade:", "Descrição:", "Estado (UF):"]
        entries = {}
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry

        def limpar_campos():
            """Função para limpar os widgets de entrada."""
            for entry_widget in entries.values():
                entry_widget.delete(0, 'end') 
            messagebox.showinfo("Limpeza", "Formulário limpo com sucesso.")

        def submeter():
            try:
                cod = int(entries["Código da Cidade:"].get())
                if self.cidades_db.incluir_cidade(cod, entries["Descrição:"].get(), entries["Estado (UF):"].get()):
                    messagebox.showinfo("Sucesso", f"Cidade {cod} incluída.")
                    limpar_campos()
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Verifique o console.")
            except ValueError: messagebox.showerror("Erro de Input", "O Código deve ser um número inteiro.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")

        button_group = ctk.CTkFrame(form_sub_frame, fg_color="transparent")
        button_group.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ctk.CTkButton(button_group, text="Salvar Cidade", command=submeter).pack(side="left", padx=10)
        ctk.CTkButton(button_group, text="Limpar Campos", command=limpar_campos, fg_color="gray", hover_color="#555555").pack(side="left", padx=10)

    def _criar_form_especialidades(self):
        """Cria os campos para a entidade Especialidades."""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10)
        form_sub_frame.grid_columnconfigure(1, weight=1)

        fields = ["Código:", "Descrição:", "Valor da Consulta:", "Limite Diário:"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry
        
        def limpar_campos():
            for entry_widget in entries.values():
                entry_widget.delete(0, 'end') 
            messagebox.showinfo("Limpeza", "Formulário limpo com sucesso.")

        def submeter():
            try:
                cod = int(entries["Código:"].get()); desc = entries["Descrição:"].get()
                valor = float(entries["Valor da Consulta:"].get()); limite = int(entries["Limite Diário:"].get())
                if self.especialidades_db.incluir_especialidade(cod, desc, valor, limite):
                    messagebox.showinfo("Sucesso", f"Especialidade {desc} incluída.")
                    limpar_campos()
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Código duplicado ou inválido.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Código, Valor e Limite são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
            
        button_group = ctk.CTkFrame(form_sub_frame, fg_color="transparent")
        button_group.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ctk.CTkButton(button_group, text="Salvar Especialidade", command=submeter).pack(side="left", padx=10)
        ctk.CTkButton(button_group, text="Limpar Campos", command=limpar_campos, fg_color="gray", hover_color="#555555").pack(side="left", padx=10)
    
    def _criar_form_pacientes(self):
        """Cria os campos para a entidade Pacientes."""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10)
        form_sub_frame.grid_columnconfigure(1, weight=1)
        
        fields = ["Código:", "Nome:", "Data Nasc. (AAAAMMDD):", "Endereço:", "Telefone:", "Cod. Cidade:", "Peso (kg):", "Altura (cm):"]
        entries = {}
        i = -1 
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry
            
        def limpar_campos():
            for entry_widget in entries.values():
                entry_widget.delete(0, 'end') 
            messagebox.showinfo("Limpeza", "Formulário limpo com sucesso.")
            
        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código:"])
                cod_cidade = int(dados["Cod. Cidade:"])
                peso = float(dados["Peso (kg):"])
                altura = float(dados["Altura (cm):"])
                
                if self.pacientes_db.incluir_paciente(cod, dados["Nome:"], dados["Data Nasc. (AAAAMMDD):"], dados["Endereço:"], dados["Telefone:"], cod_cidade, peso, altura):
                    messagebox.showinfo("Sucesso", f"Paciente {dados['Nome:']} incluído.")
                    limpar_campos()
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Cidade não existe ou Código duplicado.")
            except ValueError:
                messagebox.showerror("Erro de Input", "Verifique se Código, Cidade, Peso e Altura são números válidos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

        button_group = ctk.CTkFrame(form_sub_frame, fg_color="transparent")
        button_group.grid(row=i+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(button_group, text="Salvar Paciente", command=submeter).pack(side="left", padx=10)
        ctk.CTkButton(button_group, text="Limpar Campos", command=limpar_campos, fg_color="gray", hover_color="#555555").pack(side="left", padx=10)

    def _criar_form_medicos(self):
        """Cria os campos para a entidade Médicos."""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10)
        form_sub_frame.grid_columnconfigure(1, weight=1)
        
        fields = ["Código:", "Nome:", "Endereço:", "Telefone:", "Cod. Cidade:", "Cod. Especialidade:"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry
            
        def limpar_campos():
            for entry_widget in entries.values():
                entry_widget.delete(0, 'end') 
            messagebox.showinfo("Limpeza", "Formulário limpo com sucesso.")

        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código:"]); cod_cidade = int(dados["Cod. Cidade:"])
                cod_especialidade = int(dados["Cod. Especialidade:"])
                
                if self.medicos_db.incluir_medico(cod, dados["Nome:"], dados["Endereço:"], dados["Telefone:"], cod_cidade, cod_especialidade):
                    messagebox.showinfo("Sucesso", f"Médico {dados['Nome:']} incluído.")
                    limpar_campos()
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Cidade/Especialidade inválida ou Código duplicado.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Códigos são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
            
        button_group = ctk.CTkFrame(form_sub_frame, fg_color="transparent")
        button_group.grid(row=len(fields), column=0, columnspan=2, pady=20)
            
        ctk.CTkButton(button_group, text="Salvar Médico", command=submeter).pack(side="left", padx=10)
        ctk.CTkButton(button_group, text="Limpar Campos", command=limpar_campos, fg_color="gray", hover_color="#555555").pack(side="left", padx=10)

    def _criar_form_exames(self):
        """Cria os campos para a entidade Exames."""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10)
        form_sub_frame.grid_columnconfigure(1, weight=1)
        
        fields = ["Código:", "Descrição:", "Cod. Especialidade:", "Valor do Exame:"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry
            
        def limpar_campos():
            for entry_widget in entries.values():
                entry_widget.delete(0, 'end') 
            messagebox.showinfo("Limpeza", "Formulário limpo com sucesso.")

        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código:"]); cod_especialidade = int(dados["Cod. Especialidade:"])
                valor = float(dados["Valor do Exame:"])
                
                if self.exames_db.incluir_exame(cod, dados["Descrição:"], cod_especialidade, valor):
                    messagebox.showinfo("Sucesso", f"Exame {dados['Descrição:']} incluído.")
                    limpar_campos()
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Especialidade inválida ou Código duplicado.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Códigos e Valor são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
        
        button_group = ctk.CTkFrame(form_sub_frame, fg_color="transparent")
        button_group.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_group, text="Salvar Exame", command=submeter).pack(side="left", padx=10)
        ctk.CTkButton(button_group, text="Limpar Campos", command=limpar_campos, fg_color="gray", hover_color="#555555").pack(side="left", padx=10)

    def _criar_form_consultas(self):
        """Cria os campos para a entidade Consultas."""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10)
        form_sub_frame.grid_columnconfigure(1, weight=1)
        
        fields = ["Código da Consulta:", "Cód. Paciente:", "Cód. Médico:", "Cód. Exame:", "Data (AAAAMMDD):", "Hora (HH:MM):"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry

        def limpar_campos():
            for entry_widget in entries.values():
                entry_widget.delete(0, 'end') 
            messagebox.showinfo("Limpeza", "Formulário limpo com sucesso.")
            
        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código da Consulta:"]); cod_paciente = int(dados["Cód. Paciente:"])
                cod_medico = int(dados["Cód. Médico:"]); cod_exame = int(dados["Cód. Exame:"])
                
                if self.consultas_db.incluir_consulta(cod, cod_paciente, cod_medico, cod_exame, dados["Data (AAAAMMDD):"], dados["Hora (HH:MM):"]):
                    messagebox.showinfo("Sucesso", f"Consulta {cod} agendada!")
                    limpar_campos()
                else:
                    messagebox.showerror("Erro", "Falha no agendamento. Verifique limite diário ou chaves no console.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Códigos são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")

        button_group = ctk.CTkFrame(form_sub_frame, fg_color="transparent")
        button_group.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_group, text="Agendar Consulta", command=submeter).pack(side="left", padx=10)
        ctk.CTkButton(button_group, text="Limpar Campos", command=limpar_campos, fg_color="gray", hover_color="#555555").pack(side="left", padx=10)


    # ======================================================================
    # ABA 2: CONSULTAS & RELATÓRIOS (ITENS 6 E 7)
    # ======================================================================

    def _setup_relatorios_tab(self):
        """Configura a interface de consultas e relatórios, com botões Item 6 e 7."""
        frame = self.notebook.tab("Consultas & Relatórios")
        
        # --- CONSULTA RÁPIDA (Item 1.2/1.3) ---
        ctk.CTkLabel(frame, text="CONSULTA E EXCLUSÃO POR CÓDIGO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.consulta_entry = ctk.CTkEntry(frame, placeholder_text="Código da Consulta para Buscar/Excluir")
        self.consulta_entry.pack(pady=5, padx=20)
        
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=5)

        ctk.CTkButton(button_frame, text="Buscar Consulta", command=self._buscar_consulta_gui).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Excluir Consulta", command=self._excluir_consulta_gui, fg_color="red").pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Limpar Área", command=self._limpar_area_consulta, fg_color="gray", hover_color="#555555").pack(side="left", padx=10) 
        
        self.resultado_label = ctk.CTkTextbox(frame, height=120, width=800)
        self.resultado_label.pack(pady=10, padx=20)

        # --- RELATÓRIOS (Itens 6 e 7) ---
        ctk.CTkLabel(frame, text="RELATÓRIOS DE FATURAMENTO E ORDENAÇÃO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        
        report_frame_row1 = ctk.CTkFrame(frame, fg_color="transparent")
        report_frame_row1.pack(pady=5)
        
        report_frame_row2 = ctk.CTkFrame(frame, fg_color="transparent")
        report_frame_row2.pack(pady=5)

        # Linha 1: Faturamento (Dia, Período, Médico)
        ctk.CTkButton(report_frame_row1, text="6.1 Faturamento por Dia", command=lambda: self._executar_relatorio_faturamento("dia")).pack(side="left", padx=5)
        ctk.CTkButton(report_frame_row1, text="6.2 Faturamento por Período", command=lambda: self._executar_relatorio_faturamento("periodo")).pack(side="left", padx=5) 
        ctk.CTkButton(report_frame_row1, text="6.3 Faturamento por Médico", command=lambda: self._executar_relatorio_faturamento("medico")).pack(side="left", padx=5)
        
        # Linha 2: Faturamento (Especialidade) e Relatório Completo
        ctk.CTkButton(report_frame_row2, text="6.4 Faturamento por Especialidade", command=lambda: self._executar_relatorio_faturamento("especialidade")).pack(side="left", padx=5)
        ctk.CTkButton(report_frame_row2, text="7. RELATÓRIO ORDENADO (ITEM 7)", command=self._executar_relatorio_ordenado).pack(side="left", padx=5)

    def _limpar_area_consulta(self):
        """Limpa o campo de entrada e o resultado da consulta rápida."""
        self.consulta_entry.delete(0, 'end')
        self.resultado_label.delete("1.0", "end")
        messagebox.showinfo("Limpeza", "Área de consulta limpa.")

    def _buscar_consulta_gui(self):
        """Busca a consulta na GUI e exibe o resultado (Item 5)."""
        try:
            cod = int(self.consulta_entry.get())
            consulta = self.consultas_db.consultar_consulta(cod)
            
            self.resultado_label.delete("1.0", "end")
            if consulta:
                output = f"CÓDIGO: {consulta['codigo']} | DATA: {consulta['data']} | HORA: {consulta['hora']}\n"
                output += f"PACIENTE: {consulta['nome_paciente']} ({consulta['nome_cidade_paciente']})\n"
                output += f"MÉDICO: {consulta['nome_medico']} ({consulta.get('especialidade_desc', 'N/A')})\n"
                output += f"EXAME: {consulta['desc_exame']} | IMC: {consulta.get('imc', 'N/A')} ({consulta.get('diagnostico_imc', 'N/A')})\n"
                output += f"VALOR TOTAL: R$ {consulta['valor_total_a_pagar']:.2f}\n"
                self.resultado_label.insert("1.0", output)
            else:
                self.resultado_label.insert("1.0", "Consulta não encontrada ou código inválido.")
        except ValueError:
            messagebox.showerror("Erro de Input", "Código da consulta deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")
            
    def _excluir_consulta_gui(self):
        """Exclui a consulta na GUI (Item 5.4)."""
        try:
            cod = int(self.consulta_entry.get())
            if self.consultas_db.excluir_consulta(cod):
                messagebox.showinfo("Sucesso", f"Consulta {cod} excluída (logicamente) e vaga liberada.")
                self.resultado_label.delete("1.0", "end")
                self.resultado_label.insert("1.0", f"Consulta {cod} excluída com sucesso.")
            else:
                messagebox.showerror("Erro", f"Consulta {cod} não pode ser excluída. Verifique o código.")
        except ValueError:
            messagebox.showerror("Erro de Input", "Código da consulta deve ser um número inteiro.")

    def _display_report_details(self, lista_consultas, titulo, filtro_valor=None):
        """Método auxiliar para formatar e exibir os detalhes dos relatórios na GUI."""
        valor_total_geral = sum(c.get('valor_total_a_pagar', 0.0) for c in lista_consultas)
        
        output = "\n" + "="*80 + "\n"
        output += f"RELATÓRIO: {titulo}\n"
        output += "="*80 + "\n"

        if filtro_valor:
            output += f"Filtro: {filtro_valor}\n"
            output += "-"*80 + "\n"

        if not lista_consultas:
            output += "Nenhum registro encontrado para este filtro.\n"
        else:
            for c in lista_consultas:
                output += f"Cód: {c['codigo']} ({c.get('data', 'N/A')}) | Paciente: {c['nome_paciente']}\n"
                output += f"  > Médico: {c['nome_medico']} | Valor: R$ {c['valor_total_a_pagar']:.2f}\n"
                output += "-"*80 + "\n"
            
        output += "\n" + "="*80 + "\n"
        output += f"VALOR TOTAL: R$ {valor_total_geral:.2f}\n"

        self.resultado_label.delete("1.0", "end") 
        self.resultado_label.insert("1.0", output)
        
        return valor_total_geral

    def _executar_relatorio_faturamento(self, tipo):
        
        try:
            reports = []
            filtro = ""
            
            if tipo == "dia":
                data_raw = ctk.CTkInputDialog(text="Digite a DATA (AAAAMMDD, ex: 20251130):", title="Faturamento por Dia").get_input()
                if not data_raw: return
                
                
                data = data_raw.replace('/', '').replace('-', '').replace(' ', '')
                
                if not data.isdigit() or len(data) != 8: 
                    messagebox.showerror("Erro de Formato", "A data deve conter 8 dígitos numéricos (AAAAMMDD).")
                    return
                
                reports = self.consultas_db.faturamento_por_dia(data)
                titulo = "Faturamento por Dia"; filtro = f"Data: {data}"
            
            elif tipo == "periodo":
                data_inicial_raw = ctk.CTkInputDialog(text="Digite a DATA INICIAL (AAAAMMDD):", title="Faturamento por Período").get_input()
                if not data_inicial_raw: return
                data_final_raw = ctk.CTkInputDialog(text="Digite a DATA FINAL (AAAAMMDD):", title="Faturamento por Período").get_input()
                if not data_final_raw: return

                # CRÍTICO: Limpeza de input para Período
                data_inicial = data_inicial_raw.replace('/', '').replace('-', '').replace(' ', '')
                data_final = data_final_raw.replace('/', '').replace('-', '').replace(' ', '')
                
                if not (data_inicial.isdigit() and len(data_inicial) == 8 and data_final.isdigit() and len(data_final) == 8):
                    messagebox.showerror("Erro de Formato", "Ambas as datas devem conter 8 dígitos numéricos (AAAAMMDD).")
                    return

                reports = self.consultas_db.faturamento_por_periodo(data_inicial, data_final)
                titulo = "Faturamento por Período"; filtro = f"Período: {data_inicial} a {data_final}"
                        
            elif tipo == "medico":
                cod_str = ctk.CTkInputDialog(text="Digite o CÓDIGO do Médico:", title="Faturamento por Médico").get_input()
                if not cod_str or not cod_str.isdigit(): return
                reports = self.consultas_db.faturamento_por_medico(int(cod_str))
                titulo = "Faturamento por Médico"; filtro = f"Código: {cod_str}"
            
            elif tipo == "especialidade":
                cod_esp_str = ctk.CTkInputDialog(text="Digite o CÓDIGO da Especialidade:", title="Faturamento por Especialidade").get_input()
                if not cod_esp_str or not cod_esp_str.isdigit(): return
                reports = self.consultas_db.faturamento_por_especialidade(int(cod_esp_str))
                titulo = "Faturamento por Especialidade"; filtro = f"Código: {cod_esp_str}"
            
            # Exibe o resultado na área de texto da GUI
            if reports is not None:
                self._display_report_details(reports, titulo, filtro)

        except ValueError as e:
            messagebox.showerror("Erro de Input", f"Código ou Data inválida. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro de Processamento", f"Ocorreu um erro na lógica de faturamento. Detalhes: {e}")

    def _executar_relatorio_ordenado(self):
        """Executa o relatório ordenado e exibe o resultado (Item 7)."""
        self.resultado_label.delete("1.0", "end")
        self.resultado_label.insert("1.0", "Gerando Relatório Ordenado (Item 7). Aguarde o processamento...")
        
        try:
            lista_consultas = self.consultas_db.relatorio_ordenado()
            
            valor_total_geral = sum(c['valor_total_a_pagar'] for c in lista_consultas)
            total_pacientes_atendidos = len(set(c['cod_paciente'] for c in lista_consultas))
            
            output = "\n" + "="*80 + "\n"
            output += "RELATÓRIO DE CONSULTAS ORDENADO POR CÓDIGO (ITEM 7)\n"
            output += "="*80 + "\n"
            
            for c in lista_consultas:
                output += f"Cód: {c['codigo']} | Paciente: {c['nome_paciente']} (IMC: {c['imc']} - {c['diagnostico_imc']})\n"
                output += f"  > Médico: {c['nome_medico']} | Exame: {c['desc_exame']} | Valor: R$ {c['valor_total_a_pagar']:.2f}\n"
                output += "-"*80 + "\n"
                
            output += "\n" + "="*80 + "\n"
            output += f"QUANTIDADE TOTAL DE REGISTROS: {len(lista_consultas)}\n"
            output += f"QUANTIDADE TOTAL DE PACIENTES ATENDIDOS: {total_pacientes_atendidos}\n"
            output += f"VALOR TOTAL GERAL A SER PAGO: R$ {valor_total_geral:.2f}\n"
            
            self.resultado_label.delete("1.0", "end") 
            self.resultado_label.insert("1.0", output)
            messagebox.showinfo("Relatório Concluído", f"Valor Total Geral a Pagar: R$ {valor_total_geral:.2f}. Detalhes na tela.")
            
        except Exception as e:
             messagebox.showerror("Erro", f"Erro ao gerar relatório ordenado: {e}")
             self.resultado_label.insert("end", f"\nERRO: {e}")


if __name__ == "__main__":
    try:
        app = ClinicaApp()
        app.mainloop()
    except Exception as e:
        print(f"ERRO CRÍTICO NA INICIALIZAÇÃO DA APP: {e}")