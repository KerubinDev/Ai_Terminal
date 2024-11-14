from dataclasses import dataclass
from typing import Dict, Any
import json
import os

@dataclass
class ConfiguracaoIA:
    """Configurações da IA Kerubin."""
    prompt_sistema: str
    temperatura: float
    max_tokens: int
    modelo: str
    idioma_padrao: str
    
    @classmethod
    def carregar_padrao(cls) -> 'ConfiguracaoIA':
        return cls(
            prompt_sistema=(
                "Você é Kerubin, uma IA assistente amigável e prestativa. "
                "Você deve sempre responder em português do Brasil de forma "
                "natural e contextual. Seu objetivo é ajudar os usuários com "
                "suas dúvidas e tarefas, mantendo um tom profissional mas "
                "acolhedor."
            ),
            temperatura=0.7,
            max_tokens=2000,
            modelo="gpt-3.5-turbo",
            idioma_padrao="pt-BR"
        )
    
    def salvar(self, caminho: str) -> None:
        """Salva as configurações em arquivo JSON."""
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)
    
    @classmethod
    def carregar(cls, caminho: str) -> 'ConfiguracaoIA':
        """Carrega configurações de arquivo JSON."""
        if not os.path.exists(caminho):
            config = cls.carregar_padrao()
            config.salvar(caminho)
            return config
            
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return cls(**dados) 