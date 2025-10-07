

import os 

import ArvoreBinaria.persistencia as persistencia_mod
import ArvoreBinaria.ArvoreBinaria as arvore_mod

class BaseDados:
   
    def __init__(self, nome_entidade):
        self.nome_entidade = nome_entidade
        self.gerenciador_arquivo = persistencia_mod.GerenciadorArquivo(f'{nome_entidade}.txt')
        self.indice = arvore_mod.ArvoreBinaria()
        self._carregar_indice() # CRÍTICO: Carrega o índice ao iniciar cada DAO

    def _carregar_indice(self):
        try:
            # Acessa o arquivo para varrer linha por linha
            with open(self.gerenciador_arquivo.nome_arquivo, 'r', encoding='utf-8') as f:
                endereco_atual = 0
                while True:
                    #  Registra o offset ANTES de ler a linha
                    endereco_atual = f.tell() 
                    linha = f.readline() 
                    
                    if not linha:
                        break # Fim do arquivo
                    
                    registro = linha.strip()
                    # Ignora registros logicamente excluídos (começados por '*')
                    if registro and not registro.startswith('*'):
                        
                        try:
                            # A chave (código) é sempre o primeiro campo
                            chave = registro.split('|')[0]
                            # Tenta converter para int. Se a chave for string, remove o int()
                            chave = int(chave) 
                            self.indice.inserir(chave, endereco_atual)
                        except ValueError:
                            # Ignora linhas inválidas se o primeiro campo não for numérico
                            pass 

        except FileNotFoundError:
            pass # O arquivo será criado na primeira inclusão

    def incluir(self, registro_dados, chave):
    
        endereco = self.gerenciador_arquivo.gravar_registro(registro_dados)
     
        self.indice.inserir(chave, endereco)
        return True

    def buscar_por_chave(self, chave):
    
        endereco = self.indice.buscar(chave)
        
        if endereco is None:
            return None 
        
      
        return self.gerenciador_arquivo.ler_registro_por_endereco(endereco)

    def excluir_por_chave(self, chave):
    
        endereco = self.indice.buscar(chave)
        
        if endereco is None:
            return False 
        
     
        if self.gerenciador_arquivo.excluir_registro(endereco):
         
            return True 
        
        return False

    def ler_todos(self):
       
        return self.gerenciador_arquivo.ler_arquivo_exaustivo()