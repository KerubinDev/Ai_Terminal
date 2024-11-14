from typing import Dict
from src.utils.gerenciador_conversas import GerenciadorConversas
from src.utils.gerenciador_arquivos import GerenciadorArquivos
from src.assistente.processador_linguagem import ProcessadorLinguagem
from src.assistente.provedor_ia import ProvedorIA, RespostaIA
from cerebro.memoria.memoria_ia import MemoriaIA
from datetime import datetime
from src.assistente.processador_linguagem_avancado import ProcessadorLinguagemAvancado
from src.cerebro.aprendizado.aprendizado_continuo import AprendizadoContinuo
from src.integracao.integrador_apis import IntegradorAPIs

class ChatIA:
    """Assistente de IA para processamento de mensagens."""
    
    def __init__(self, gerenciador_arquivos: GerenciadorArquivos):
        self._gerenciador = gerenciador_arquivos
        self._perfil_usuario = self._carregar_perfil()
        self._gerenciador_conversas = GerenciadorConversas()
        self._processador = ProcessadorLinguagem()
        self._provedor_ia = ProvedorIA(gerenciador=self._gerenciador)
        self._memoria = MemoriaIA()
        self._conversa_atual_id = None
        self._processador_avancado = ProcessadorLinguagemAvancado()
        self._aprendizado = AprendizadoContinuo()
        self._integrador_apis = IntegradorAPIs()
    
    async def processar_mensagem(self, texto: str) -> str:
        try:
            if not self._conversa_atual_id:
                nome_conversa = await self._gerar_nome_conversa(texto)
                self._conversa_atual_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_conversa}"
                self._gerenciador.salvar_log(
                    f"Nova conversa iniciada: {self._conversa_atual_id}"
                )
                self._gerenciador_conversas.adicionar_mensagem(
                    texto, "usuario", self._conversa_atual_id
                )
                self.salvar_conversa_atual()
            
            self._gerenciador.salvar_log(
                f"Processando mensagem na conversa {self._conversa_atual_id}"
            )
            
            # Análise de sentimento
            sentimento = self._processador_avancado.analisar_sentimento(texto)
            
            # Extração de entidades
            entidades = self._processador_avancado.extrair_entidades(texto)
            
            # Busca informações externas se necessário
            info_externa = await self._integrador_apis.buscar_informacao(
                "wikipedia", texto
            )
            
            # Monta o contexto enriquecido
            contexto = self._montar_contexto_enriquecido(
                texto, sentimento, entidades, info_externa
            )
            
            # Obtém resposta da IA
            resposta = await self._obter_resposta_ia(contexto)
            
            texto_resposta = resposta.texto if hasattr(resposta, 'texto') else str(resposta)
            
            # Aprende com a interação
            self._aprendizado.aprender_com_interacao(
                texto, texto_resposta, feedback=5
            )
            
            return texto_resposta
            
        except Exception as e:
            self.registrar_erro(f"Erro no processamento avançado: {str(e)}")
            resposta_fallback = await self._obter_resposta_ia(texto)
            return str(resposta_fallback)
    
    def _carregar_perfil(self) -> Dict:
        return self._gerenciador.carregar_perfil()
    
    async def _obter_resposta_ia(self, texto: str) -> RespostaIA:
        """Obtém resposta da IA incluindo contexto da memória."""
        contexto = self._memoria.obter_contexto()
        prompt_completo = f"{contexto}\nUsuário: {texto}\n\nKerubin:"
        
        resposta = await self._provedor_ia.obter_resposta_async(prompt_completo)
        
        if resposta.sucesso:
            self._memoria.adicionar_interacao(texto, resposta.texto)
            
        return resposta
    
    def registrar_erro(self, mensagem: str) -> None:
        self._gerenciador.salvar_log(mensagem)
    
    def salvar_conversa_atual(self) -> None:
        """Salva a conversa atual."""
        try:
            if self._conversa_atual_id:
                caminho = self._gerenciador_conversas.salvar_conversa()
                if caminho:
                    self._gerenciador.salvar_log(f"Conversa salva em: {caminho}")
                    self._gerenciador_conversas.limpar_conversas_antigas()
        except Exception as e:
            self._gerenciador.salvar_log(f"Erro ao salvar conversa: {str(e)}") 
    
    async def _gerar_nome_conversa(self, texto: str) -> str:
        """Gera um nome personalizado para a conversa baseado no contexto."""
        try:
            prompt = (
                "Com base nas primeiras 5 mensagens do usuário, crie um título curto e "
                "descritivo para esta conversa (máximo 50 caracteres). "
                f"Mensagem: {texto}"
            )
            
            resposta = await self._provedor_ia.obter_resposta_async(prompt)
            if resposta.sucesso:
                return resposta.texto.strip()
        except Exception as e:
            self.registrar_erro(f"Erro ao gerar nome da conversa: {str(e)}")
        
        return datetime.now().strftime("%Y%m%d_%H%M%S")