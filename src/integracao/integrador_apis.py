import aiohttp
from typing import Dict, Optional
import json
import os

class IntegradorAPIs:
    """Integrador de APIs externas."""
    
    def __init__(self):
        self._carregar_configuracoes()
        self._session = None
    
    async def inicializar(self):
        """Inicializa a sessão HTTP."""
        if not self._session:
            self._session = aiohttp.ClientSession()
    
    async def buscar_informacao(self, tipo: str, query: str) -> Optional[Dict]:
        """Busca informações em APIs externas."""
        await self.inicializar()
        
        if tipo not in self._apis:
            return None
            
        api_config = self._apis[tipo]
        url = api_config['url'].format(query=query)
        
        async with self._session.get(url, headers=api_config['headers']) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
    
    def _carregar_configuracoes(self):
        """Carrega configurações das APIs."""
        config_path = os.path.join(
            os.path.expanduser("~"),
            ".kerubin",
            "config",
            "apis.json"
        )
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self._apis = json.load(f)
        else:
            self._apis = self._criar_config_padrao()
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self._apis, f, indent=4)
    
    def _criar_config_padrao(self) -> Dict:
        """Cria configuração padrão para as APIs."""
        return {
            "wikipedia": {
                "url": "https://pt.wikipedia.org/api/rest_v1/page/summary/{query}",
                "headers": {
                    "User-Agent": "KerubinIA/1.0"
                }
            },
            "noticias": {
                "url": "https://newsapi.org/v2/everything?q={query}&language=pt",
                "headers": {
                    "X-Api-Key": "sua_chave_api_aqui"
                }
            },
            "clima": {
                "url": "http://api.openweathermap.org/data/2.5/weather?q={query}&lang=pt_br",
                "headers": {
                    "appid": "sua_chave_api_aqui"
                }
            },
            "traducao": {
                "url": "https://translation.googleapis.com/language/translate/v2?q={query}",
                "headers": {
                    "Authorization": "Bearer sua_chave_api_aqui"
                }
            }
        }