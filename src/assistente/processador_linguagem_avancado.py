from textblob import TextBlob
import spacy
from typing import Dict, Optional
import json
import os

class ProcessadorLinguagemAvancado:
    """Processador avançado de linguagem natural."""
    
    def __init__(self):
        try:
            self._nlp = spacy.load('pt_core_news_lg')
        except OSError:
            # Se o modelo não estiver instalado, baixa automaticamente
            os.system('python -m spacy download pt_core_news_lg')
            self._nlp = spacy.load('pt_core_news_lg')
        
    def analisar_sentimento(self, texto: str) -> Dict:
        """Analisa o sentimento do texto."""
        analise = TextBlob(texto)
        return {
            'polaridade': analise.sentiment.polarity,
            'subjetividade': analise.sentiment.subjectivity
        }
    
    def extrair_entidades(self, texto: str) -> Dict:
        """Extrai entidades nomeadas do texto."""
        doc = self._nlp(texto)
        entidades = {}
        for ent in doc.ents:
            if ent.label_ not in entidades:
                entidades[ent.label_] = []
            entidades[ent.label_].append(ent.text)
        return entidades
    
    def sumarizar_texto(self, texto: str, max_sentencas: int = 3) -> str:
        """Gera um resumo do texto."""
        doc = self._nlp(texto)
        return " ".join([sent.text for sent in doc.sents][:max_sentencas]) 