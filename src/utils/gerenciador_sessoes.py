from typing import List, Dict, Optional
from datetime import datetime
import os
import json
import glob

class GerenciadorSessoes:
    """Gerenciador de sessões de conversas."""
    
    def __init__(self, diretorio_base: str = None):
        if diretorio_base is None:
            home = os.path.expanduser("~")
            diretorio_base = os.path.join(home, ".kerubin", "conversas")
        self._diretorio_base = diretorio_base
        os.makedirs(diretorio_base, exist_ok=True)
    
    def listar_conversas(self) -> List[Dict]:
        """Lista todas as conversas salvas."""
        conversas = []
        arquivos = glob.glob(os.path.join(self._diretorio_base, "conversa_*.json"))
        
        for arquivo in sorted(arquivos, reverse=True):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    nome_arquivo = os.path.basename(arquivo)
                    id_completo = nome_arquivo.replace('conversa_', '').replace('.json', '')
                    
                    # Extrai o nome personalizado do ID
                    partes = id_completo.split('_', 3)
                    nome_personalizado = partes[3] if len(partes) > 3 else id_completo
                    
                    mensagens = dados.get('mensagens', [])
                    primeira_msg = next((m for m in mensagens if m['tipo'] == 'usuario'), None)
                    ultima_msg = next((m for m in reversed(mensagens) if m['tipo'] == 'usuario'), None)
                    
                    conversas.append({
                        'id': id_completo,
                        'nome': nome_personalizado,
                        'data_inicio': dados.get('data_inicio', ''),
                        'primeira_mensagem': primeira_msg.get('texto', '') if primeira_msg else '',
                        'ultima_mensagem': ultima_msg.get('texto', '') if ultima_msg else '',
                        'total_mensagens': len(mensagens)
                    })
            except Exception:
                continue
                
        return conversas
    
    def carregar_conversa(self, id_conversa: str) -> Optional[Dict]:
        """Carrega uma conversa específica."""
        caminho = os.path.join(self._diretorio_base, f"conversa_{id_conversa}.json")
        
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados
        else:
            return None 
    
    def excluir_conversa(self, id_conversa: str) -> bool:
        """Exclui uma conversa específica pelo ID."""
        try:
            caminho = os.path.join(self._diretorio_base, f"conversa_{id_conversa}.json")
            if os.path.exists(caminho):
                os.remove(caminho)
                return True
            return False
        except Exception as e:
            raise Exception(f"Erro ao excluir conversa: {str(e)}")