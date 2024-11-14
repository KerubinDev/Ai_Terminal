import g4f
from typing import Tuple, List, Optional
from dataclasses import dataclass
import nest_asyncio
import asyncio
import platform

nest_asyncio.apply()  # Permite nested event loops

@dataclass
class RespostaIA:
    """Classe para armazenar resposta da IA."""
    texto: str
    provedor: str
    sucesso: bool = True

class ProvedorIA:
    """Gerenciador de provedores de IA."""
    
    def __init__(self, gerenciador=None):
        self._gerenciador = gerenciador
        self._providers = [
            ('FreeGpt', g4f.Provider.FreeGpt),
            ('You', g4f.Provider.You),
            ('ChatAnywhere', g4f.Provider.ChatAnywhere)
        ]
        
        # Configura o event loop
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy()
            )
        
    async def obter_resposta_async(self, texto: str) -> RespostaIA:
        """Versão assíncrona de obter_resposta."""
        erros = []
        
        for nome, provedor in self._providers:
            try:
                if self._gerenciador:
                    self._gerenciador.salvar_log(
                        f"Tentando obter resposta com provedor: {nome}"
                    )
                
                resposta = await g4f.ChatCompletion.create_async(
                    model="gpt-3.5-turbo",
                    provider=provedor,
                    messages=[{
                        "role": "system",
                        "content": (
                            "Você é um assistente amigável chamado Kerubin. "
                            "Responda em português do Brasil de forma natural. "
                            "Use markdown para formatar suas respostas."
                        )
                    }, {
                        "role": "user",
                        "content": texto
                    }]
                )
                
                if resposta and len(resposta.strip()) > 0:
                    if self._gerenciador:
                        self._gerenciador.salvar_log(
                            f"Resposta obtida com sucesso do provedor: {nome}"
                        )
                    return RespostaIA(texto=resposta, provedor=nome)
                    
            except Exception as e:
                erro_msg = f"{nome}: {str(e)}"
                if self._gerenciador:
                    self._gerenciador.salvar_log(f"Erro no provedor {nome}: {erro_msg}")
                erros.append(erro_msg)
                continue
        
        return RespostaIA(
            texto="Desculpe, não consegui gerar uma resposta no momento.",
            provedor="Fallback",
            sucesso=False
        ) 