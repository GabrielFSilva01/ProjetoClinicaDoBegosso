🏥 Sistema de Gestão Clínica - Arquivos Indexados (Python/Tkinter)
Este projeto simula um sistema de gerenciamento para uma clínica médica utilizando a arquitetura clássica de Arquivos Indexados (ISAM). O sistema utiliza uma Árvore Binária de Busca (BST) em memória para o índice e arquivos de texto em disco para a persistência dos dados (Área de Dados). A interface é construída com CustomTkinter para uma experiência amigável.

🌟 Destaques do Projeto
Arquitetura Híbrida: Separação clara entre a Área de Índices (em memória - Árvore Binária) e a Área de Dados (em disco - arquivos .txt).

Acesso Indexado Rápido: Todas as operações de busca, inclusão e exclusão utilizam o endereço de byte offset (posição) fornecido pela Árvore Binária para acesso instantâneo ao disco.

Regras de Negócio Robustas: Implementação de lógica complexa como cálculo de IMC, verificação de Limite Diário de Consultas e Cálculo de Faturamento.

Relatórios Avançados: Geração de relatórios ordenados (via percurso in-order da Árvore Binária) e diversos filtros de faturamento.

Interface Gráfica (GUI): Frontend moderno e intuitivo construído com CustomTkinter.

🛠️ Tecnologias e Dependências
Linguagem: Python 3.8+

Frontend (GUI): customtkinter (Baseado em Tkinter)

Instalação das Dependências
Para rodar a interface gráfica, você precisará instalar a biblioteca customtkinter:

Bash

pip install customtkinter
🚀 Como Executar o Sistema
Siga estes passos para iniciar a aplicação:

Clone o repositório (ou garanta que todos os arquivos .py estejam no mesmo diretório).

Verifique a estrutura de arquivos:

main.py (Ponto de entrada)

interface_app.py (Frontend Tkinter)

arvore_binaria.py, persistencia.py, base_dados.py (Core do Sistema de Arquivos Indexados)

cidades.py, pacientes.py, consultas.py, etc. (Entidades/Tabelas)

Execute o arquivo principal:

Bash

python main.py
A aplicação GUI (ClinicaApp) será iniciada imediatamente. Ao fechar a janela, todos os dados cadastrados serão salvos automaticamente nos arquivos de dados (Cidades.txt, Pacientes.txt, etc.).

📖 Estrutura das Entidades (Tabelas)
O sistema gerencia as seguintes entidades, com a chave primária sendo utilizada como o índice na Árvore Binária:

Tabela	Chave Primária	Relacionamentos e Lógica
Cidades	Código da Cidade	Base de referência.
Especialidades	Código da Especialidade	Define o Valor e o Limite Diário de consultas.
Pacientes	Código do Paciente	Relaciona-se com Cidades. Calcula o IMC.
Médicos	Código do Médico	Relaciona-se com Cidades e Especialidades.
Exames	Código do Exame	Relaciona-se com Especialidades.
Consultas	Código da Consulta	Pivô central. Relaciona-se com TODAS as entidades. Controla o Limite Diário (via tabela Diárias) e o Faturamento.
Diárias	Chave Composta (Data + Especialidade)	Tabela auxiliar para controle de vagas (Incremento/Decremento).

Exportar para as Planilhas
✨ Funcionalidades Implementadas
O projeto cobre integralmente os requisitos de gestão de dados:

Requisito	Descrição	Localização na GUI
Item 1.1	Inclusão de Novos Registros	Aba Cadastro Manual
Itens 1.2, 1.3	Consulta e Exclusão (Indexada)	Aba Consultas & Relatórios
Item 2.1	Cálculo e Exibição do IMC	Ocorre na Consulta do Paciente.
Item 5.1	Verificação do Limite Diário	Ocorre no cadastro de Consultas.
Item 6	Relatórios de Faturamento (Dia, Médico, Especialidade, Período)	Aba Consultas & Relatórios
Item 7	Listagem em Ordem Crescente	Botão Relatório Ordenado (Utiliza o percurso In-Order da Árvore Binária)

Exportar para as Planilhas
👤 Desenvolvedor
Este projeto foi desenvolvido por Gabriel Ferreira e Thiago Henrique do Segundo ano de BCC na FEMA
