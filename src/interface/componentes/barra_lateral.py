from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QScrollArea,
                            QLabel, QFrame, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List, Dict
import json

class BarraLateral(QWidget):
    """Barra lateral com histórico de conversas."""
    
    conversa_selecionada = pyqtSignal(str)  # Sinal para conversa selecionada
    nova_conversa = pyqtSignal()  # Sinal para nova conversa
    
    def __init__(self, gerenciador_sessoes, parent=None):
        super().__init__(parent)
        self._gerenciador_sessoes = gerenciador_sessoes
        self._configurar_interface()
        self._conversas: List[Dict] = []
        
    def _configurar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Botão Nova Conversa
        btn_nova = QPushButton("+ Nova Conversa")
        btn_nova.setStyleSheet("""
            QPushButton {
                background-color: #202123;
                color: white;
                border: 1px solid #565869;
                padding: 10px;
                border-radius: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2A2B32;
            }
        """)
        btn_nova.clicked.connect(self.nova_conversa.emit)
        layout.addWidget(btn_nova)
        
        # Área de conversas com barra de rolagem moderna
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none;
                background-color: #202123;
            }
            QScrollBar:vertical {
                border: none;
                background: #202123;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #565869;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        self._container_conversas = QWidget()
        self._layout_conversas = QVBoxLayout(self._container_conversas)
        self._layout_conversas.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self._container_conversas)
        
        layout.addWidget(scroll)
        
    def atualizar_conversas(self, conversas: List[Dict]):
        """Atualiza a lista de conversas."""
        self._conversas = conversas[-10:]  # Mantém apenas as 10 últimas
        self._limpar_conversas()
        
        for conversa in self._conversas:
            container = QWidget()
            layout_container = QHBoxLayout(container)
            layout_container.setContentsMargins(5, 2, 5, 2)
            
            # Botão principal com informações da conversa
            btn = QPushButton()
            layout_btn = QVBoxLayout(btn)
            layout_btn.setContentsMargins(10, 5, 10, 5)
            
            data = QLabel(conversa['data_inicio'])
            data.setStyleSheet("color: #888888; font-size: 9pt;")
            
            mensagem = QLabel(conversa['primeira_mensagem'][:40] + "...")
            mensagem.setStyleSheet("color: white; font-size: 10pt;")
            mensagem.setWordWrap(True)
            
            layout_btn.addWidget(data)
            layout_btn.addWidget(mensagem)
            
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #202123;
                    border: none;
                    border-radius: 5px;
                    text-align: left;
                    min-height: 60px;
                }
                QPushButton:hover {
                    background-color: #2A2B32;
                }
            """)
            
            btn.clicked.connect(
                lambda checked, id=conversa['id']: self.conversa_selecionada.emit(id)
            )
            
            # Botão de exclusão
            btn_excluir = QPushButton("×")
            btn_excluir.setFixedSize(24, 24)
            btn_excluir.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #888888;
                    border: none;
                    font-size: 16pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff4444;
                }
            """)
            btn_excluir.clicked.connect(
                lambda checked, id=conversa['id']: self._excluir_conversa(id)
            )
            
            layout_container.addWidget(btn, stretch=1)
            layout_container.addWidget(btn_excluir)
            self._layout_conversas.addWidget(container)
            
    def _limpar_conversas(self):
        """Remove todos os botões de conversas."""
        while self._layout_conversas.count():
            item = self._layout_conversas.takeAt(0)
            if item.widget():
                item.widget().deleteLater() 
    
    def _excluir_conversa(self, id_conversa: str):
        """Exclui uma conversa específica."""
        resposta = QMessageBox.question(
            self,
            "Excluir Conversa",
            "Tem certeza que deseja excluir esta conversa?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            try:
                self._gerenciador_sessoes.excluir_conversa(id_conversa)
                # Emite sinal para nova conversa para atualizar a interface
                self.nova_conversa.emit()
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Erro",
                    f"Erro ao excluir conversa: {str(e)}"
                )