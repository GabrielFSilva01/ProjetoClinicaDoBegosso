

import customtkinter as ctk
from tkinter import messagebox, simpledialog 
from datetime import datetime



import  Classes.Cidade as cid_mod
import Classes.Especialidades as esp_mod
import Classes.Pacientes as pac_mod
import Classes.Medicos as med_mod
import Classes.Exames as exa_mod
import Classes.Consultas as con_mod

class ClinicaApp(ctk.CTk):
    """Classe principal da aplicação com interface gráfica (GUI)."""
    
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Clínica - Arquivos Indexados")
        self.geometry("800x650") # Aumentei a altura para melhor visualização

        # --- Inicialização do Backend ---
        self.cidades_db = cid_mod.Cidades()
        self.especialidades_db = esp_mod.Especialidades()
        self.pacientes_db = pac_mod.Pacientes()
        self.medicos_db = med_mod.Medicos()
        self.exames_db = exa_mod.Exames()
        self.consultas_db = con_mod.Consultas()

        # --- Criação do Notebook (Abas) ---
        self.notebook = ctk.CTkTabview(self, width=780, height=580)
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)

        self.notebook.add("Cadastro Manual")
        self.notebook.add("Consultas & Relatórios")
        
        self._setup_cadastro_tab()
        self._setup_relatorios_tab()

    # ======================================================================
    # ABA 1: CADASTRO MANUAL (ITEM 1.1)
    # ======================================================================

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
        # self.form_container USA PACK
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
        
    # --- IMPLEMENTAÇÃO DOS FORMULÁRIOS COM CORREÇÃO DE GRID/PACK ---

    def _criar_form_cidades(self):
        """Cria os campos para a entidade Cidades."""
        # Novo frame interno para usar GRID
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10) 
        form_sub_frame.grid_columnconfigure(1, weight=1) # Faz a coluna de entrada expandir

        fields = ["Código da Cidade:", "Descrição:", "Estado (UF):"]
        entries = {}
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry

        def submeter():
            try:
                cod = int(entries["Código da Cidade:"].get())
                if self.cidades_db.incluir_cidade(cod, entries["Descrição:"].get(), entries["Estado (UF):"].get()):
                    messagebox.showinfo("Sucesso", f"Cidade {cod} incluída.")
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Verifique o console.")
            except ValueError: messagebox.showerror("Erro de Input", "O Código deve ser um número inteiro.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")

        ctk.CTkButton(form_sub_frame, text="Salvar Cidade", command=submeter).grid(row=len(fields), column=0, columnspan=2, pady=20)

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
        
        def submeter():
            try:
                cod = int(entries["Código:"].get()); desc = entries["Descrição:"].get()
                valor = float(entries["Valor da Consulta:"].get()); limite = int(entries["Limite Diário:"].get())
                if self.especialidades_db.incluir_especialidade(cod, desc, valor, limite):
                    messagebox.showinfo("Sucesso", f"Especialidade {desc} incluída.")
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Código duplicado ou inválido.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Código, Valor e Limite são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
        ctk.CTkButton(form_sub_frame, text="Salvar Especialidade", command=submeter).grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    def _criar_form_pacientes(self):
        """Cria os campos para a entidade Pacientes. (Correção do 'i' aplicada)"""
        form_sub_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_sub_frame.pack(fill="x", padx=20, pady=10)
        form_sub_frame.grid_columnconfigure(1, weight=1)
        
        fields = ["Código:", "Nome:", "Data Nasc. (AAAAMMDD):", "Endereço:", "Telefone:", "Cod. Cidade:", "Peso (kg):", "Altura (cm):"]
        entries = {}
        
        i = -1 # Inicialização de 'i' para evitar o erro de unbound
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_sub_frame, text=field, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_sub_frame, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[field] = entry
            
        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código:"])
                cod_cidade = int(dados["Cod. Cidade:"])
                peso = float(dados["Peso (kg):"])
                altura = float(dados["Altura (cm):"])
                
                if self.pacientes_db.incluir_paciente(cod, dados["Nome:"], dados["Data Nasc. (AAAAMMDD):"], dados["Endereço:"], dados["Telefone:"], cod_cidade, peso, altura):
                    messagebox.showinfo("Sucesso", f"Paciente {dados['Nome:']} incluído.")
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Cidade não existe ou Código duplicado.")
            except ValueError:
                messagebox.showerror("Erro de Input", "Verifique se Código, Cidade, Peso e Altura são números válidos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

        # O botão usa o último 'i' válido + 1
        ctk.CTkButton(form_sub_frame, text="Salvar Paciente", command=submeter).grid(row=i+1, column=0, columnspan=2, pady=20)


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
            
        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código:"]); cod_cidade = int(dados["Cod. Cidade:"])
                cod_especialidade = int(dados["Cod. Especialidade:"])
                
                if self.medicos_db.incluir_medico(cod, dados["Nome:"], dados["Endereço:"], dados["Telefone:"], cod_cidade, cod_especialidade):
                    messagebox.showinfo("Sucesso", f"Médico {dados['Nome:']} incluído.")
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Cidade/Especialidade inválida ou Código duplicado.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Códigos são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
            
        ctk.CTkButton(form_sub_frame, text="Salvar Médico", command=submeter).grid(row=len(fields), column=0, columnspan=2, pady=20)

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
            
        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código:"]); cod_especialidade = int(dados["Cod. Especialidade:"])
                valor = float(dados["Valor do Exame:"])
                
                if self.exames_db.incluir_exame(cod, dados["Descrição:"], cod_especialidade, valor):
                    messagebox.showinfo("Sucesso", f"Exame {dados['Descrição:']} incluído.")
                else:
                    messagebox.showerror("Erro", "Falha na inclusão. Especialidade inválida ou Código duplicado.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Códigos e Valor são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
        
        ctk.CTkButton(form_sub_frame, text="Salvar Exame", command=submeter).grid(row=len(fields), column=0, columnspan=2, pady=20)

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

        def submeter():
            try:
                dados = {k: entries[k].get() for k in entries}
                cod = int(dados["Código da Consulta:"]); cod_paciente = int(dados["Cód. Paciente:"])
                cod_medico = int(dados["Cód. Médico:"]); cod_exame = int(dados["Cód. Exame:"])
                
                # A inclusão valida o limite diário e as chaves estrangeiras (Item 5)
                if self.consultas_db.incluir_consulta(cod, cod_paciente, cod_medico, cod_exame, dados["Data (AAAAMMDD):"], dados["Hora (HH:MM):"]):
                    messagebox.showinfo("Sucesso", f"Consulta {cod} agendada!")
                else:
                    messagebox.showerror("Erro", "Falha no agendamento. Verifique limite diário ou chaves no console.")
            except ValueError: messagebox.showerror("Erro de Input", "Verifique se Códigos são números válidos.")
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")

        ctk.CTkButton(form_sub_frame, text="Agendar Consulta", command=submeter).grid(row=len(fields), column=0, columnspan=2, pady=20)


    # ======================================================================
    # ABA 2: CONSULTAS & RELATÓRIOS (ITENS 6 E 7)
    # ======================================================================

    def _setup_relatorios_tab(self):
        """Configura a interface de consultas e relatórios."""
        frame = self.notebook.tab("Consultas & Relatórios")
        
        # --- CONSULTA RÁPIDA (Item 1.2) ---
        ctk.CTkLabel(frame, text="CONSULTA E EXCLUSÃO POR CÓDIGO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.consulta_entry = ctk.CTkEntry(frame, placeholder_text="Código da Consulta para Buscar/Excluir")
        self.consulta_entry.pack(pady=5, padx=20)
        
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=5)

        ctk.CTkButton(button_frame, text="Buscar Consulta", command=self._buscar_consulta_gui).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Excluir Consulta", command=self._excluir_consulta_gui, fg_color="red").pack(side="left", padx=10)
        
        self.resultado_label = ctk.CTkTextbox(frame, height=120, width=500)
        self.resultado_label.pack(pady=10)

        # --- RELATÓRIOS (Itens 6 e 7) ---
        ctk.CTkLabel(frame, text="RELATÓRIOS DE FATURAMENTO E ORDENAÇÃO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        
        report_frame = ctk.CTkFrame(frame, fg_color="transparent")
        report_frame.pack(pady=5)
        
        ctk.CTkButton(report_frame, text="1. Faturamento por Dia", command=lambda: self._executar_relatorio_faturamento("dia")).pack(side="left", padx=5)
        ctk.CTkButton(report_frame, text="2. Faturamento por Médico", command=lambda: self._executar_relatorio_faturamento("medico")).pack(side="left", padx=5)
        ctk.CTkButton(report_frame, text="3. RELATÓRIO ORDENADO (ITEM 7)", command=self._executar_relatorio_ordenado).pack(side="left", padx=5)


    def _buscar_consulta_gui(self):
        """Busca a consulta na GUI e exibe o resultado (Item 5)."""
        try:
            cod = int(self.consulta_entry.get())
            consulta = self.consultas_db.consultar_consulta(cod)
            
            self.resultado_label.delete("1.0", "end")
            if consulta:
                output = f"CÓDIGO: {consulta['codigo']} | DATA: {consulta['data']}\n"
                output += f"PACIENTE: {consulta['nome_paciente']} ({consulta['nome_cidade_paciente']})\n"
                output += f"MÉDICO: {consulta['nome_medico']} ({consulta.get('especialidade_desc', 'N/A')})\n"
                output += f"EXAME: {consulta['desc_exame']}\n"
                output += f"VALOR TOTAL: R$ {consulta['valor_total_a_pagar']:.2f}\n"
                self.resultado_label.insert("1.0", output)
            else:
                self.resultado_label.insert("1.0", "Consulta não encontrada ou código inválido.")
        except ValueError:
            messagebox.showerror("Erro de Input", "Código da consulta deve ser um número inteiro.")

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

    def _executar_relatorio_faturamento(self, tipo):
        """Executa um relatório de faturamento simples (Item 6)."""
        try:
            if tipo == "dia":
                data = ctk.CTkInputDialog(text="Digite a DATA (AAAAMMDD):", title="Faturamento por Dia").get_input()
                if data:
                    faturamento = self.consultas_db.faturamento_por_dia(data)
                    messagebox.showinfo("Faturamento", f"O Faturamento total para {data} foi de R$ {faturamento:.2f}. Detalhes no console.")
            elif tipo == "medico":
                cod = ctk.CTkInputDialog(text="Digite o CÓDIGO do Médico:", title="Faturamento por Médico").get_input()
                if cod:
                    faturamento = self.consultas_db.faturamento_por_medico(int(cod))
                    messagebox.showinfo("Faturamento", f"Faturamento do Médico {cod}: R$ {faturamento:.2f}. Detalhes no console.")
            # Faltam os relatórios por Período e Especialidade, mas o padrão está aqui.

        except ValueError:
            messagebox.showerror("Erro de Input", "Código ou Data inválida.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def _executar_relatorio_ordenado(self):
        """Executa o relatório ordenado e exibe o resultado (Item 7)."""
        self.resultado_label.delete("1.0", "end")
        self.resultado_label.insert("1.0", "Gerando Relatório Ordenado (Item 7). Verifique o console para a saída completa e totais.")
        
        total = self.consultas_db.relatorio_ordenado()
        
        messagebox.showinfo("Relatório Concluído", f"Valor Total Geral a Pagar: R$ {total:.2f}. Detalhes completos no console.")


if __name__ == "__main__":
    # Este bloco deve estar no seu arquivo 'main.py' real
    app = ClinicaApp()
    app.mainloop()