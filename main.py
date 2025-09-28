# main.py - O PONTO DE ENTRADA FINAL DO SEU PROJETO

# Importa a classe principal da sua interface gráfica
# Certifique-se de que o arquivo interface_app.py está na mesma pasta.
from interface_app import ClinicaApp

def main():
    """
    Função principal que inicia a aplicação GUI (CustomTkinter).
    """
    print("Iniciando o Sistema de Gestão Clínica (GUI)...")
    
    # 1. Cria a instância da aplicação ClinicaApp
    app = ClinicaApp()
    
    # 2. Inicia o loop principal da interface gráfica
    app.mainloop()
    
    # Esta mensagem aparece no console assim que a janela da aplicação é fechada.
    print("Aplicação encerrada. Os dados foram salvos no disco.")

if __name__ == "__main__":
    main()