from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTextEdit, QLineEdit, QPushButton, QLabel, QFrame,
                            QDialog, QSpinBox, QDoubleSpinBox, QFormLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor
from src.assistente.chat_ia import ChatIA
from src.utils.gerenciador_arquivos import GerenciadorArquivos
from config.configuracao_ia import ConfiguracaoIA
from src.interface.componentes.barra_lateral import BarraLateral
from src.utils.gerenciador_sessoes import GerenciadorSessoes
from src.assistente.provedor_ia import RespostaIA
import asyncio
import qasync
import markdown2
import platform

class DialogoConfiguracao(QDialog):
    """Diálogo para configuração da IA."""
    
    def __init__(self, config: ConfiguracaoIA, parent=None):
        super().__init__(parent)
        self.config = config
        self._configurar_interface()
    
    def _configurar_interface(self):
        self.setWindowTitle("Configurações do Kerubin")
        layout = QFormLayout(self)
        
        # Prompt do sistema
        self.prompt = QTextEdit(self.config.prompt_sistema)
        layout.addRow("Prompt do Sistema:", self.prompt)
        
        # Temperatura
        self.temperatura = QDoubleSpinBox()
        self.temperatura.setRange(0.1, 1.0)
        self.temperatura.setSingleStep(0.1)
        self.temperatura.setValue(self.config.temperatura)
        layout.addRow("Temperatura:", self.temperatura)
        
        # Tokens máximos
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(100, 4000)
        self.max_tokens.setSingleStep(100)
        self.max_tokens.setValue(self.config.max_tokens)
        layout.addRow("Tokens Máximos:", self.max_tokens)
        
        # Botões
        botoes = QHBoxLayout()
        salvar = QPushButton("Salvar")
        cancelar = QPushButton("Cancelar")
        
        salvar.clicked.connect(self.accept)
        cancelar.clicked.connect(self.reject)
        
        botoes.addWidget(salvar)
        botoes.addWidget(cancelar)
        layout.addRow(botoes)
        
    def obter_configuracao(self) -> ConfiguracaoIA:
        return ConfiguracaoIA(
            prompt_sistema=self.prompt.toPlainText(),
            temperatura=self.temperatura.value(),
            max_tokens=self.max_tokens.value(),
            modelo=self.config.modelo,
            idioma_padrao=self.config.idioma_padrao
        ) 

class JanelaPrincipal(QMainWindow):
    """Janela principal da aplicação Kerubin."""
    
    def __init__(self, gerenciador: GerenciadorArquivos):
        super().__init__()
        
        # Configura o event loop correto para Windows
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        self._gerenciador = gerenciador
        self._config = ConfiguracaoIA.carregar("config/kerubin.json")
        self._chat_ia = ChatIA(gerenciador)
        self._gerenciador_sessoes = GerenciadorSessoes()
        self._processando_mensagem = False
        self._configurar_interface()
        self._carregar_conversas()
        
        # Configura o loop de eventos assíncrono
        self._loop = qasync.QEventLoop()
        asyncio.set_event_loop(self._loop)
    
    def _configurar_interface(self):
        self.setWindowTitle("Kerubin IA")
        self.setMinimumSize(1200, 600)
        self._configurar_estilo()
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout = QHBoxLayout(widget_central)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Container da barra lateral
        self._container_lateral = QWidget()
        self._container_lateral.setFixedWidth(280)
        self._container_lateral.setStyleSheet("background-color: #202123;")
        layout_lateral = QHBoxLayout(self._container_lateral)
        layout_lateral.setContentsMargins(0, 0, 0, 0)
        layout_lateral.setSpacing(0)
        
        # Botão para retrair/expandir
        btn_toggle = QPushButton("≡")
        btn_toggle.setFixedWidth(30)
        btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: #202123;
                color: white;
                border: none;
                padding: 5px;
                font-size: 16pt;
            }
            QPushButton:hover {
                background-color: #2A2B32;
            }
        """)
        btn_toggle.clicked.connect(self._toggle_barra_lateral)
        
        # Barra Lateral
        self._barra_lateral = BarraLateral(self._gerenciador_sessoes)
        self._barra_lateral.setFixedWidth(250)
        self._barra_lateral.conversa_selecionada.connect(self._carregar_conversa)
        self._barra_lateral.nova_conversa.connect(self._nova_conversa)
        
        layout_lateral.addWidget(btn_toggle)
        layout_lateral.addWidget(self._barra_lateral)
        
        # Container principal do chat
        container_chat = QWidget()
        container_chat.setStyleSheet("background-color: #343541;")
        layout_chat = QVBoxLayout(container_chat)
        layout_chat.setContentsMargins(20, 20, 20, 20)
        
        # Área de histórico
        self._historico = QTextEdit()
        self._historico.setReadOnly(True)
        self._historico.setStyleSheet("""
            QTextEdit {
                background-color: #343541;
                color: white;
                border: none;
                font-family: 'Segoe UI';
                font-size: 11pt;
            }
        """)
        layout_chat.addWidget(self._historico)
        
        # Container de entrada
        container_entrada = QWidget()
        container_entrada.setStyleSheet("background-color: #40414F;")
        layout_entrada = QHBoxLayout(container_entrada)
        layout_entrada.setContentsMargins(10, 10, 10, 10)
        
        # Campo de entrada
        self._entrada = QLineEdit()
        self._entrada.setPlaceholderText("Digite sua mensagem...")
        self._entrada.setStyleSheet("""
            QLineEdit {
                background-color: #40414F;
                color: white;
                border: 1px solid #565869;
                border-radius: 5px;
                padding: 10px;
                font-size: 11pt;
            }
        """)
        self._entrada.returnPressed.connect(self._processar_mensagem)
        
        # Botão de configurações
        btn_config = QPushButton("⚙️")
        btn_config.setFixedSize(40, 40)
        btn_config.setStyleSheet("""
            QPushButton {
                background-color: #40414F;
                color: white;
                border: 1px solid #565869;
                border-radius: 5px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #2A2B32;
            }
        """)
        btn_config.clicked.connect(self._abrir_configuracoes)
        
        layout_entrada.addWidget(self._entrada)
        layout_entrada.addWidget(btn_config)
        layout_chat.addWidget(container_entrada)
        
        # Adiciona widgets ao layout principal
        layout.addWidget(self._container_lateral)
        layout.addWidget(container_chat)
    
    def _toggle_barra_lateral(self):
        """Alterna visibilidade da barra lateral com animação."""
        largura_atual = self._container_lateral.width()
        largura_final = 30 if largura_atual > 30 else 280
        
        self._animacao = QPropertyAnimation(self._container_lateral, b"minimumWidth")
        self._animacao.setDuration(200)
        self._animacao.setStartValue(largura_atual)
        self._animacao.setEndValue(largura_final)
        self._animacao.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._animacao.start()
        
        # Esconde/mostra widgets
        if largura_final == 30:
            self._barra_lateral.hide()
        else:
            self._barra_lateral.show()
    
    def _carregar_conversas(self):
        """Carrega e exibe conversas salvas."""
        conversas = self._gerenciador_sessoes.listar_conversas()
        self._barra_lateral.atualizar_conversas(conversas)
    
    def _nova_conversa(self):
        """Inicia uma nova conversa."""
        self._historico.clear()
        self._chat_ia._conversa_atual_id = None  # Limpa ID atual
        self._chat_ia._memoria._historico.clear()  # Limpa histórico
        self._chat_ia.salvar_conversa_atual()
        self._carregar_conversas()
    
    def _configurar_estilo(self):
        """Configura o estilo dark da interface."""
        paleta = QPalette()
        paleta.setColor(QPalette.ColorRole.Window, QColor("#343541"))
        paleta.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
        self.setPalette(paleta)
    
    async def _enviar_mensagem(self):
        """Processa e envia a mensagem do usuário."""
        if self._processando_mensagem:
            return
            
        texto = self._entrada.text().strip()
        if not texto:
            return
        
        try:
            self._processando_mensagem = True
            self._entrada.setEnabled(False)
            self._entrada.setPlaceholderText("Aguarde a resposta...")
            
            # Limpa o campo de entrada
            self._entrada.clear()
            
            # Adiciona a mensagem do usuário ao histórico
            mensagem_usuario = self._formatar_mensagem(texto, "usuario")
            self._historico.append(mensagem_usuario)
            
            # Obtém a resposta da IA de forma assíncrona
            resposta = await self._chat_ia.processar_mensagem(texto)
            
            # Converte a resposta para HTML e adiciona ao histórico
            if resposta:
                # Extrai apenas o texto da resposta se for um objeto RespostaIA
                texto_resposta = (
                    resposta.texto if isinstance(resposta, RespostaIA)
                    else str(resposta)
                )
                resposta_html = self._converter_markdown_para_html(texto_resposta)
                mensagem_ia = self._formatar_mensagem(resposta_html, "assistente")
                self._historico.append(mensagem_ia)
        
        except Exception as e:
            erro = f"Erro ao processar mensagem: {str(e)}"
            self._historico.append(self._formatar_mensagem(erro, "erro"))
        
        finally:
            self._processando_mensagem = False
            self._entrada.setEnabled(True)
            self._entrada.setPlaceholderText("Digite sua mensagem...")
            self._entrada.setFocus()
            
            # Rola para o final do histórico
            self._historico.verticalScrollBar().setValue(
                self._historico.verticalScrollBar().maximum()
            )
    
    def _converter_markdown_para_html(self, texto: str) -> str:
        """Converte texto markdown para HTML."""
        try:
            extras = [
                "fenced-code-blocks",
                "tables",
                "header-ids",
                "task_list",
                "code-friendly"
            ]
            
            # Remove caracteres de nova linha extras
            texto = texto.replace('\n\n\n', '\n\n')
            
            # Garante que o texto é uma string
            if not isinstance(texto, str):
                texto = str(texto)
                
            html = markdown2.markdown(texto, extras=extras)
            
            # Adiciona CSS para estilização
            css = """
            <style>
                code { 
                    background-color: #2d2d2d; 
                    padding: 2px 4px; 
                    border-radius: 3px; 
                }
                pre { 
                    background-color: #2d2d2d; 
                    padding: 10px; 
                    border-radius: 5px; 
                    overflow-x: auto; 
                }
                h3 {
                    margin-top: 0;
                    margin-bottom: 10px;
                    color: #c9c9c9;
                }
                p {
                    margin: 5px 0;
                }
            </style>
            """
            return css + html
        except Exception as e:
            print(f"Erro ao converter markdown: {str(e)}")
            return texto
    
    def _abrir_configuracoes(self):
        dialogo = DialogoConfiguracao(self._config, self)
        if dialogo.exec():
            self._config = dialogo.obter_configuracao()
            self._config.salvar("config/kerubin.json")
    
    async def closeEvent(self, event):
        """Manipula o evento de fechamento da janela."""
        try:
            # Salva a conversa atual
            self._chat_ia.salvar_conversa_atual()
            
            # Fecha todas as sessões pendentes
            if hasattr(self._chat_ia._provedor_ia, '_session'):
                await self._chat_ia._provedor_ia._session.close()
            
            # Limpa o event loop
            pending = asyncio.all_tasks(self._loop)
            for task in pending:
                task.cancel()
            
            await asyncio.gather(*pending, return_exceptions=True)
            
        except Exception as e:
            print(f"Erro ao fechar aplicação: {e}")
        finally:
            event.accept()
    
    def _adicionar_mensagem_historico(self, texto: str) -> None:
        """Adiciona uma mensagem ao histórico com formatação HTML."""
        texto_html = self._converter_markdown_para_html(texto)
        self._historico.insertHtml(texto_html)
        self._historico.insertHtml("<hr>")
        # Rola para o final
        self._historico.verticalScrollBar().setValue(
            self._historico.verticalScrollBar().maximum()
        )
    
    def _carregar_conversa(self, id_conversa: str) -> None:
        """Carrega uma conversa específica."""
        conversa = self._gerenciador_sessoes.carregar_conversa(id_conversa)
        if not conversa:
            return
        
        self._historico.clear()
        mensagens = conversa['mensagens']
        
        for mensagem in mensagens:
            origem = "Você" if mensagem['tipo'] == 'usuario' else "Kerubin"
            texto = f"### {origem}\n{mensagem['texto']}"
            self._adicionar_mensagem_historico(texto)
        
        # Atualiza o ID da conversa atual
        self._chat_ia._conversa_atual_id = id_conversa
    
    def _formatar_mensagem(self, texto: str, tipo: str) -> str:
        """Formata a mensagem para exibição no histórico."""
        # Remove caracteres de escape e formatação extra
        texto = texto.replace('\\n', '\n').strip()
        
        # Remove a representação do objeto RespostaIA se presente
        if tipo == "assistente" and "RespostaIA" in texto:
            try:
                texto = eval(texto).texto
            except:
                if "texto='" in texto:
                    texto = texto.split("texto='")[1].split("'")[0]
        
        css_usuario = """
            background-color: #343541;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        """
        
        css_assistente = """
            background-color: #444654;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        """
        
        css_erro = """
            background-color: #6e1a1a;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        """
        
        if tipo == "usuario":
            icone = "👤"
            css = css_usuario
        elif tipo == "assistente":
            icone = "🤖"
            css = css_assistente
        else:  # erro
            icone = "⚠️"
            css = css_erro
        
        return f"""
            <div style="{css}">
                <p style="margin: 0;"><strong>{icone} {tipo.title()}</strong></p>
                <div style="margin-top: 5px;">{texto}</div>
            </div>
        """
    
    def _processar_mensagem(self):
        """Wrapper para processar mensagem de forma assíncrona."""
        try:
            self._loop.create_task(self._enviar_mensagem())
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")