from src.assistente.chat_ia import ChatIA
from src.utils.gerenciador_arquivos import GerenciadorArquivos
from src.utils.gerenciador_sessoes import GerenciadorSessoes
from typing import Optional

class ChatInterface:
    """Interface de chat com o usuário."""
    
    def __init__(self, gerenciador: GerenciadorArquivos):
        self._chat_ia = ChatIA(gerenciador)
        self._gerenciador_sessoes = GerenciadorSessoes()
        self._executando = False
        self._conversa_atual: Optional[str] = None
    
    def iniciar(self) -> None:
        """Inicia a interface de chat."""
        self._executando = True
        self._exibir_menu_principal()
        
        while self._executando:
            try:
                self._processar_comando()
            except KeyboardInterrupt:
                self._finalizar()
                break
            except Exception as e:
                print("\nErro ao processar comando.")
                self._chat_ia.registrar_erro(str(e))
    
    def _exibir_menu_principal(self) -> None:
        """Exibe o menu principal da interface."""
        print("\n=== Kerubin IA ===")
        print("1. Nova Conversa")
        print("2. Carregar Conversa")
        print("3. Sair")
    
    def _processar_comando(self) -> None:
        """Processa o comando escolhido pelo usuário."""
        comando = input("\nEscolha uma opção: ").strip()
        
        if comando == "1":
            self._iniciar_nova_conversa()
        elif comando == "2":
            self._exibir_conversas_salvas()
        elif comando == "3":
            self._finalizar()
        elif self._conversa_atual:
            self._processar_mensagem(comando)
    
    def _exibir_conversas_salvas(self) -> None:
        """Exibe as conversas salvas disponíveis."""
        conversas = self._gerenciador_sessoes.listar_conversas()
        
        if not conversas:
            print("\nNenhuma conversa encontrada.")
            return
            
        print("\n=== Conversas Salvas ===")
        for i, conversa in enumerate(conversas, 1):
            print(f"\n{i}. Data: {conversa['data_inicio']}")
            print(f"   Primeira mensagem: {conversa['primeira_mensagem'][:50]}...")
            print(f"   Última mensagem: {conversa['ultima_mensagem'][:50]}...")
            print(f"   Total de mensagens: {conversa['total_mensagens']}")
        
        escolha = input("\nEscolha uma conversa para continuar (0 para voltar): ")
        if escolha.isdigit() and 0 < int(escolha) <= len(conversas):
            self._carregar_conversa(conversas[int(escolha)-1]['id'])
    
    def _carregar_conversa(self, id_conversa: str) -> None:
        """Carrega uma conversa específica."""
        conversa = self._gerenciador_sessoes.carregar_conversa(id_conversa)
        if conversa:
            self._conversa_atual = id_conversa
            print("\n=== Conversa Carregada ===")
            for msg in conversa['mensagens']:
                origem = "Você" if msg['tipo'] == 'usuario' else "Kerubin"
                print(f"\n{origem} ({msg['timestamp']}): {msg['texto']}")
    
    def _finalizar(self) -> None:
        """Finaliza a interface e salva dados."""
        self._executando = False
        self._chat_ia.salvar_conversa_atual()
        print("\nAté logo!")