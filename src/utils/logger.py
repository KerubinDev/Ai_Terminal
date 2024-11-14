from datetime import datetime
import os

class Logger:
    """Gerenciador de logs do sistema."""
    
    def __init__(self, diretorio: str = None):
        if diretorio is None:
            home = os.path.expanduser("~")
            diretorio = os.path.join(home, ".kerubin", "logs")
        self._diretorio = diretorio
        self._criar_diretorio()
        
    def _criar_diretorio(self) -> None:
        os.makedirs(self._diretorio, exist_ok=True)
    
    def registrar(self, mensagem: str) -> None:
        data_atual = datetime.now().strftime("%Y-%m-%d")
        arquivo_log = os.path.join(self._diretorio, f"log_{data_atual}.txt")
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        linha_log = f"[{timestamp}] {mensagem}\n"
        
        with open(arquivo_log, 'a', encoding='utf-8') as f:
            f.write(linha_log)
