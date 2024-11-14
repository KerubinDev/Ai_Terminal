"""Módulo principal da aplicação."""
from PyQt6.QtWidgets import QApplication
from src.interface.janela_principal import JanelaPrincipal
from src.utils.gerenciador_arquivos import GerenciadorArquivos
from src.utils.logger import Logger
import sys
import asyncio
import qasync

async def main():
    app = QApplication(sys.argv)
    logger = Logger()
    gerenciador = GerenciadorArquivos(logger=logger)
    janela = JanelaPrincipal(gerenciador)
    janela.show()
    
    # Configura o loop de eventos do qasync
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Executa a aplicação
    await loop.run_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Erro na execução: {str(e)}") 