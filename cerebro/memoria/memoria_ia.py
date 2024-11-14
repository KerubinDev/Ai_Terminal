from typing import List, Dict
import json
import os
from datetime import datetime

class MemoriaIA:
    """Gerenciador de memória da IA."""
    
    def __init__(self, tamanho_max_contexto: int = 10):
        self._tamanho_max_contexto = tamanho_max_contexto
        self._historico: List[Dict] = []
        self._memoria_longo_prazo: List[Dict] = []
        self._carregar_memoria()
    
    def adicionar_interacao(self, mensagem: str, resposta: str) -> None:
        """Adiciona uma interação ao histórico."""
        interacao = {
            'timestamp': datetime.now().isoformat(),
            'mensagem': mensagem,
            'resposta': resposta
        }
        self._historico.append(interacao)
        
        if len(self._historico) > self._tamanho_max_contexto:
            self._arquivar_memoria(self._historico.pop(0))
    
    def obter_contexto(self) -> str:
        """Retorna o contexto atual formatado em markdown."""
        contexto = (
            "### Instruções de Formatação Markdown\n\n"
            "Use markdown avançado para formatar suas respostas de forma rica e visual:\n\n"
            
            "#### 1. Títulos e Textos\n"
            "- Use # para títulos (# h1, ## h2, ### h3)\n"
            "- Use **negrito** ou __negrito__ para ênfase forte\n"
            "- Use *itálico* ou _itálico_ para ênfase suave\n"
            "- Use ~~texto~~ para tachado\n"
            "- Use > para citações\n"
            "- Use >>> para citações aninhadas\n\n"
            
            "#### 2. Listas\n"
            "- Use - ou * para listas não ordenadas\n"
            "- Use 1. 2. 3. para listas ordenadas\n"
            "- Use    - para subníveis (4 espaços)\n"
            "- Use - [ ] para tarefas não concluídas\n"
            "- Use - [x] para tarefas concluídas\n\n"
            
            "#### 3. Tabelas\n"
            "```\n"
            "| Alinhado à Esquerda | Centralizado | Alinhado à Direita |\n"
            "|:-------------------|:------------:|------------------:|\n"
            "| Conteúdo          |   Conteúdo   |          Conteúdo |\n"
            "```\n\n"
            
            "#### 4. Gráficos ASCII/Unicode\n"
            "- Gráfico de Barras:\n"
            "```\n"
            "Vendas 2023 █████████████ 65%\n"
            "Vendas 2024 ████████████████████ 100%\n"
            "```\n"
            "- Gráfico de Linha:\n"
            "```\n"
            "┌────────── Evolução ──────────┐\n"
            "      ╭─────╮         ╭────\n"
            "    ╭─╯     ╰───╮ ╭───╯\n"
            "────╯           ╰─╯\n"
            "```\n\n"
            
            "#### 5. Blocos de Código\n"
            "- Use ` para código inline\n"
            "- Use ``` para blocos de código\n"
            "- Use ```python para código Python\n"
            "- Use ```mermaid para diagramas\n\n"
            
            "#### 6. Diagramas Mermaid\n"
            "```mermaid\n"
            "graph TD;\n"
            "    A-->B;\n"
            "    B-->C;\n"
            "    C-->D;\n"
            "```\n\n"
            
            "#### 7. Emojis e Símbolos\n"
            "- Use 👉 para indicações\n"
            "- Use ✅ para confirmações\n"
            "- Use ⚠️ para avisos\n"
            "- Use 📊 para dados\n"
            "- Use 💡 para dicas\n\n"
            
            "### Histórico recente da conversa\n\n"
        )
        
        for interacao in self._historico:
            contexto += f"#### 👤 Usuário\n{interacao['mensagem']}\n\n"
            contexto += f"#### 🤖 Kerubin\n{interacao['resposta']}\n\n"
            contexto += "---\n\n"
        
        return contexto
    
    def _arquivar_memoria(self, interacao: Dict) -> None:
        """Arquiva uma interação na memória de longo prazo."""
        self._memoria_longo_prazo.append(interacao)
        self._salvar_memoria()
    
    def _carregar_memoria(self) -> None:
        """Carrega a memória de longo prazo do arquivo."""
        home = os.path.expanduser("~")
        arquivo = os.path.join(home, ".kerubin", "memoria", "memoria_longo_prazo.json")
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                self._memoria_longo_prazo = json.load(f)
    
    def _salvar_memoria(self) -> None:
        """Salva a memória de longo prazo em arquivo."""
        home = os.path.expanduser("~")
        arquivo = os.path.join(home, ".kerubin", "memoria", "memoria_longo_prazo.json")
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(self._memoria_longo_prazo, f, ensure_ascii=False, indent=4) 