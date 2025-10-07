# arvore_binaria.py - CÓDIGO FINAL

class NoIndice:
    """Representa um nó na Árvore Binária, armazenando a chave e o endereço no arquivo."""
    def __init__(self, chave, endereco_byte):
        self.chave = chave                       # A chave de acesso (ex: Código do Paciente)
        self.endereco_byte = endereco_byte       # O 'End' ou Offset no arquivo de dados
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:

    def __init__(self):
        self.raiz = None

  
    def _inserir_recursivo(self, no_atual, chave, endereco_byte):
        if no_atual is None:
            return NoIndice(chave, endereco_byte)
        
       
        if chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave, endereco_byte)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave, endereco_byte)
        
        return no_atual

    def inserir(self, chave, endereco_byte):
        self.raiz = self._inserir_recursivo(self.raiz, chave, endereco_byte)

  
    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None:
            return None # Chave não encontrada
        if no_atual.chave == chave:
            return no_atual.endereco_byte   # Retorna o endereço (offset)
        elif chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)

    def buscar(self, chave):
        
        return self._buscar_recursivo(self.raiz, chave)
    
    
    def _percurso_recursivo_em_ordem(self, no_atual, lista_ordenada):
      
        if no_atual:
            self._percurso_recursivo_em_ordem(no_atual.esquerda, lista_ordenada)
            
            lista_ordenada.append((no_atual.chave, no_atual.endereco_byte))
            self._percurso_recursivo_em_ordem(no_atual.direita, lista_ordenada)

    def percurso_em_ordem(self):
      
        lista_ordenada = []
        self._percurso_recursivo_em_ordem(self.raiz, lista_ordenada)
        return lista_ordenada