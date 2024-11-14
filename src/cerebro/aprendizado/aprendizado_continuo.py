from datetime import datetime
from typing import Dict, List, Optional
import json
import os
import spacy
from textblob import TextBlob

class AprendizadoContinuo:
    """Sistema de aprendizado contínuo."""
    
    def __init__(self):
        self._base_conhecimento = {}
        self._feedback_usuarios = []
        self._diretorio_dados = os.path.join(
            os.path.expanduser("~"),
            ".kerubin",
            "aprendizado"
        )
        self._nlp = None
        os.makedirs(self._diretorio_dados, exist_ok=True)
        self._carregar_dados()
        self._inicializar_nlp()
    
    def _inicializar_nlp(self):
        """Inicializa o processador de linguagem natural."""
        try:
            self._nlp = spacy.load('pt_core_news_lg')
        except OSError:
            os.system('python -m spacy download pt_core_news_lg')
            self._nlp = spacy.load('pt_core_news_lg')
    
    def _extrair_palavras_chave(self, texto: str) -> List[str]:
        """Extrai palavras-chave do texto usando spaCy."""
        if not self._nlp:
            self._inicializar_nlp()
        
        doc = self._nlp(texto)
        return [
            token.text.lower() 
            for token in doc 
            if not token.is_stop and not token.is_punct and token.is_alpha
        ]
    
    def _carregar_dados(self) -> None:
        """Carrega dados de aprendizado do arquivo."""
        arquivo_conhecimento = os.path.join(
            self._diretorio_dados,
            "base_conhecimento.json"
        )
        arquivo_feedback = os.path.join(
            self._diretorio_dados,
            "feedback_usuarios.json"
        )
        
        try:
            if os.path.exists(arquivo_conhecimento):
                with open(arquivo_conhecimento, 'r', encoding='utf-8') as f:
                    self._base_conhecimento = json.load(f)
            
            if os.path.exists(arquivo_feedback):
                with open(arquivo_feedback, 'r', encoding='utf-8') as f:
                    self._feedback_usuarios = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados de aprendizado: {str(e)}")
            self._base_conhecimento = {}
            self._feedback_usuarios = []
    
    def _salvar_dados(self) -> None:
        """Salva dados de aprendizado em arquivo."""
        try:
            with open(
                os.path.join(self._diretorio_dados, "base_conhecimento.json"),
                'w',
                encoding='utf-8'
            ) as f:
                json.dump(self._base_conhecimento, f, ensure_ascii=False, indent=4)
            
            with open(
                os.path.join(self._diretorio_dados, "feedback_usuarios.json"),
                'w',
                encoding='utf-8'
            ) as f:
                json.dump(self._feedback_usuarios, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar dados de aprendizado: {str(e)}")
    
    def aprender_com_interacao(self, 
                             pergunta: str, 
                             resposta: str, 
                             feedback: int) -> None:
        """Aprende com cada interação baseado no feedback do usuário."""
        interacao = {
            'pergunta': pergunta,
            'resposta': resposta,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        }
        self._feedback_usuarios.append(interacao)
        self._atualizar_base_conhecimento(interacao)
        self._salvar_dados()
    
    def _atualizar_base_conhecimento(self, interacao: Dict) -> None:
        """Atualiza a base de conhecimento com nova interação."""
        palavras_chave = self._extrair_palavras_chave(interacao['pergunta'])
        for palavra in palavras_chave:
            if palavra not in self._base_conhecimento:
                self._base_conhecimento[palavra] = []
            self._base_conhecimento[palavra].append({
                'resposta': interacao['resposta'],
                'feedback': interacao['feedback']
            })
    
    def obter_sugestao_resposta(self, pergunta: str) -> Optional[str]:
        """Sugere uma resposta com base no histórico de interações."""
        palavras_chave = self._extrair_palavras_chave(pergunta)
        melhores_respostas = []
        
        for palavra in palavras_chave:
            if palavra in self._base_conhecimento:
                respostas = self._base_conhecimento[palavra]
                melhores_respostas.extend([
                    r['resposta'] for r in respostas 
                    if r['feedback'] >= 4
                ])
        
        return max(melhores_respostas, key=melhores_respostas.count) \
               if melhores_respostas else None 