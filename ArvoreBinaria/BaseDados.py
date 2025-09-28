import os 
# 1. Importa o módulo (o arquivo persistencia.py) e o renomeia para evitar conflitos
import ArvoreBinaria.persistencia as persistencia_mod
# 2. Importa o módulo Arvore.py e o renomeia para evitar conflitos
import ArvoreBinaria.ArvoreBinaria as arvore_mod

class BaseDados:
    """
    Classe base para todas as entidades, gerenciando a integração 
    entre o Índice (Árvore Binária) e a Área de Dados (GerenciadorArquivo).
    """
    def __init__(self, nome_entidade):
        self.nome_entidade = nome_entidade
        self.gerenciador_arquivo = persistencia_mod.GerenciadorArquivo(f'{nome_entidade}.txt')
        self.indice = arvore_mod.ArvoreBinaria()

    def _carregar_indice(self):
        """Reconstrói o Índice lendo o arquivo de dados ao iniciar o programa."""
        # Usa o GerenciadorArquivo para acessar o disco e remapear os endereços
        try:
            with open(self.gerenciador_arquivo.nome_arquivo, 'r', encoding='utf-8') as f:
                endereco_atual = 0
                while True:
                    endereco_atual = f.tell() # Posição de início do registro
                    linha = f.readline() 
                    
                    if not linha:
                        break # Fim do arquivo
                    
                    registro = linha.strip()
                    if registro and not registro.startswith('*'):
                        
                        try:
                            chave = int(registro.split('|')[0]) 
                            self.indice.inserir(chave, endereco_atual)
                        except ValueError:
                            pass 

        except FileNotFoundError:
            pass # Arquivo será criado na primeira inclusão

    def incluir(self, registro_dados, chave):
        """Inclusão (1.1): Grava no disco e insere a chave no índice."""
        endereco = self.gerenciador_arquivo.gravar_registro(registro_dados)
        self.indice.inserir(chave, endereco)
        return True

    def buscar_por_chave(self, chave):
        """Consulta (1.2): Acesso indexado. Vai do índice (chave -> endereço) para o disco."""
        endereco = self.indice.buscar(chave)
        
        if endereco is None:
            return None 
        
      
        return self.gerenciador_arquivo.ler_registro_por_endereco(endereco)

    def excluir_por_chave(self, chave):
        """Exclusão (1.3): Exclusão LÓGICA no disco e remoção no índice."""
        endereco = self.indice.buscar(chave)
        
        if endereco is None:
            return False 
        
        if self.gerenciador_arquivo.excluir_registro(endereco):
            return True
        
        return False

    def ler_todos(self):
        
        return self.gerenciador_arquivo.ler_arquivo_exaustivo()