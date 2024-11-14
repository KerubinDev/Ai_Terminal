from datetime import datetime
import os
import json
from typing import Dict, Any, Optional
from src.utils.logger import Logger

class GerenciadorArquivos:
    """Gerenciador de arquivos do sistema."""
    
    def __init__(self, logger: Logger, diretorio_base: str = None):
        self._logger = logger
        if diretorio_base is None:
            # Usa o diretório home do usuário
            home = os.path.expanduser("~")
            diretorio_base = os.path.join(home, ".kerubin", "dados")
        self._diretorio_base = diretorio_base
        self._diretorio_logs = os.path.join(diretorio_base, "logs")
        self._diretorio_perfis = os.path.join(diretorio_base, "perfis")
        self._criar_diretorios()
    
    def _criar_diretorios(self) -> None:
        """Cria os diretórios necessários se não existirem."""
        os.makedirs(self._diretorio_base, exist_ok=True)
        os.makedirs(self._diretorio_logs, exist_ok=True)
        os.makedirs(self._diretorio_perfis, exist_ok=True)
    
    def salvar_log(self, mensagem: str) -> None:
        """Salva uma mensagem no arquivo de log."""
        self._logger.registrar(mensagem)
    
    def carregar_perfil(self, nome_arquivo: str = "perfil_usuario.json") -> Dict:
        """Carrega o perfil do usuário."""
        caminho = os.path.join(self._diretorio_perfis, nome_arquivo)
        
        if not os.path.exists(caminho):
            return self._criar_perfil_padrao()
            
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.salvar_log(f"Erro ao carregar perfil: {str(e)}")
            return self._criar_perfil_padrao()
    
    def _criar_perfil_padrao(self) -> Dict[str, Any]:
        """Cria um perfil padrão."""
        return {
            "nome": None,
            "dados_pessoais": {
                "idade": None,
                "localidade": {
                    "cidade": None,
                    "estado": None,
                    "pais": None
                },
                "idioma_preferido": "português Brasileiro",
                "fuso_horario": "America/Sao_Paulo"
            },
            "preferencias": {
                "tema": "Escuro",
                "tamanho_fonte": 10,
                "som": True,
                "notificacoes": True
            }
        }
    
    def salvar_perfil(self, dados: Dict, 
                      nome_arquivo: str = "perfil_usuario.json") -> None:
        """Salva o perfil do usuário."""
        caminho = os.path.join(self._diretorio_perfis, nome_arquivo)
        
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.salvar_log(f"Erro ao salvar perfil: {str(e)}") 