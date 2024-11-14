from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import json
import os
import glob

@dataclass
class Mensagem:
    """Classe para representar uma mensagem."""
    texto: str
    tipo: str  # 'usuario' ou 'ia'
    timestamp: str = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            "texto": self.texto,
            "tipo": self.tipo,
            "timestamp": self.timestamp
        }


class GerenciadorConversas:
    """Gerenciador de conversas do sistema."""
    
    def __init__(self, diretorio_base: str = None):
        if diretorio_base is None:
            home = os.path.expanduser("~")
            diretorio_base = os.path.join(home, ".kerubin", "conversas")
        self.diretorio_base = diretorio_base
        self.conversa_atual: List[Mensagem] = []
        self._conversa_atual_id = None
        self._criar_diretorio()
    
    def _criar_diretorio(self) -> None:
        """Cria o diretório de conversas se não existir."""
        os.makedirs(self.diretorio_base, exist_ok=True)
    
    def adicionar_mensagem(self, texto: str, tipo: str, id_conversa: str = None) -> None:
        """Adiciona uma nova mensagem à conversa atual."""
        mensagem = Mensagem(texto=texto, tipo=tipo)
        
        # Se não houver ID de conversa, cria um novo
        if not id_conversa:
            id_conversa = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Se for uma nova conversa, limpa o histórico atual
        if not self.conversa_atual or self._conversa_atual_id != id_conversa:
            self.conversa_atual = []
            self._conversa_atual_id = id_conversa
        
        self.conversa_atual.append(mensagem)
    
    def salvar_conversa(self) -> Optional[str]:
        """Salva a conversa atual em arquivo."""
        if not self.conversa_atual or not self._conversa_atual_id:
            return None
        
        nome_arquivo = f"conversa_{self._conversa_atual_id}.json"
        caminho = os.path.join(self.diretorio_base, nome_arquivo)
        
        dados_conversa = {
            "id": self._conversa_atual_id,
            "data_inicio": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "mensagens": [msg.to_dict() for msg in self.conversa_atual]
        }
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados_conversa, f, ensure_ascii=False, indent=4)
        
        return caminho
    
    def limpar_conversas_antigas(self, manter: int = 5) -> None:
        """Mantém apenas as últimas N conversas."""
        arquivos = sorted(
            glob.glob(os.path.join(self.diretorio_base, "conversa_*.json")),
            reverse=True
        )
        
        for arquivo in arquivos[manter:]:
            try:
                os.remove(arquivo)
            except Exception:
                continue 