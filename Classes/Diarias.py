# diarias.py

from ArvoreBinaria.BaseDados import BaseDados

class Diarias(BaseDados):
    """
    Gerencia a tabela Diárias para controle do limite de consultas por dia/especialidade.
    Chave composta: Cod_Dia + Cod_Especialidade.
    Estrutura do arquivo: Cod_Dia|Cod_Especialidade|Quantidade
    """
    
    def __init__(self):
        super().__init__('Diarias')

    def _criar_chave_composta(self, data, cod_especialidade):
        """Cria a chave composta para busca no índice (ex: '20250928_51')."""
        return f"{data}_{cod_especialidade}" 

    def _deserializar(self, registro_string):
        """Converte a string do disco em um dicionário básico."""
        try:
            campos = registro_string.split('|')
            return {
                "codigo_dia": campos[0], 
                "cod_especialidade": int(campos[1]), 
                "quantidade": int(campos[2]), 
            }
        except Exception:
            return None

    def consultar_diaria(self, data, cod_especialidade):
        """
        Consulta a quantidade de consultas para um dia/especialidade específica.
        SEMPRE retorna um dicionário, garantindo que "quantidade" possa ser acessado.
        """
        chave = self._criar_chave_composta(data, cod_especialidade)
        registro_string = self.buscar_por_chave(chave)
        
        diaria_data = self._deserializar(registro_string)
        
        if diaria_data is None:
            # RETORNO ROBUSTO: Se não encontrado ou corrompido, simula um registro de quantidade 0.
            return {
                "codigo_dia": data, 
                "cod_especialidade": cod_especialidade, 
                "quantidade": 0, 
            }
        
        return diaria_data

    def _atualizar_registro_em_disco(self, chave, novo_registro_formatado, endereco_byte):
        """Método auxiliar para sobrescrever um registro já existente (UPDATE)."""
        try:
            with open(self.gerenciador_arquivo.nome_arquivo, 'r+', encoding='utf-8') as f:
                f.seek(endereco_byte)
                if not novo_registro_formatado.endswith('\n'):
                    novo_registro_formatado += '\n'
                
                f.write(novo_registro_formatado) 
            return True
        except Exception:
            return False

    def atualizar_quantidade(self, data, cod_especialidade, delta):
        """
        Atualiza (incrementa ou decrementa) a quantidade de consultas (Itens 5.3 e 5.4).
        """
        chave = self._criar_chave_composta(data, cod_especialidade)
        registro_string = self.buscar_por_chave(chave)
        
        # Chama a consulta que garante o retorno de um dicionário
        diaria_data = self.consultar_diaria(data, cod_especialidade) 
        
        # Acesso seguro:
        nova_quantidade = diaria_data["quantidade"] + delta 
        
        if nova_quantidade < 0:
            return False

        novo_registro_formatado = f"{data}|{cod_especialidade}|{nova_quantidade}"
        
        if registro_string is None:
            # É uma INCLUSÃO (Primeira consulta do dia/especialidade)
            if nova_quantidade > 0:
                self.incluir(novo_registro_formatado, chave)
                return True
            return False 
        else:
            endereco_byte = self.indice.buscar(chave)
            if endereco_byte is None: 
                return False 
            
            self._atualizar_registro_em_disco(chave, novo_registro_formatado, endereco_byte)
            return True