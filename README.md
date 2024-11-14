# Kerubin - Assistente Virtual Inteligente

[![License](https://img.shields.io/github/license/KerubinDev/kerubin)](LICENSE)  
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

### Índice

- [Visão Geral](#visão-geral)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Principais Funcionalidades](#principais-funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Recursos Avançados](#recursos-avançados)
- [Requisitos do Sistema](#requisitos-do-sistema)
- [Contribuições](#contribuições)
- [Licença](#licença)

---

## Visão Geral

**Kerubin** é um assistente virtual de código aberto, desenvolvido em Python, com uma interface gráfica moderna e intuitiva construída com PyQt6. Ele utiliza processamento de linguagem natural (NLP) e memória contextual para fornecer respostas dinâmicas e personalizadas. Este programa é ideal para suporte em várias áreas, como análise de dados, processamento de texto e assistência em programação.

## Arquitetura do Sistema

O Kerubin é organizado em módulos, cada um com funções específicas:

### 1. Interface do Usuário (`src/interface/janela_principal.py`)
- Interface com tema escuro e barra lateral retrátil para gerenciamento de conversas.
- Editor de texto com suporte a markdown, permitindo formatação avançada.
- Configurações personalizáveis para personalizar a experiência do usuário.

### 2. Núcleo do Assistente (`src/assistente/chat_ia.py`)
- Sistema de processamento assíncrono, com memória de curto e longo prazo.
- Análise de sentimentos e extração de entidades para respostas mais personalizadas.
- Aprendizado contínuo baseado em interações passadas.

### 3. Sistema de Memória (`cerebro/memoria/memoria_ia.py`)
- Armazenamento persistente do histórico de conversas, com formatação em markdown.
- Suporte para gráficos ASCII, diagramas e outros elementos visuais no contexto das respostas.

### 4. Gerenciamento de Sessões (`src/utils/gerenciador_sessoes.py`)
- Sistema de persistência e organização de histórico de conversas, com backup automático e limpeza de dados antigos.

## Principais Funcionalidades

### 1. Processamento de Linguagem Natural
Implementação de um pipeline para análise e resposta baseada em inteligência artificial, com uma arquitetura de resposta e memória contextuais. O sistema realiza o processamento de mensagens, salva logs e atualiza o contexto do usuário de maneira automatizada.

### 2. Sistema de Memória Contextual
Armazena interações passadas para construir respostas contextuais, enriquecendo as interações com formatação e elementos visuais em markdown, emojis, listas, e gráficos ASCII/Unicode.

### 3. Interface Gráfica Responsiva
A interface é personalizável, com opções para realizar análise de dados e processamento de texto. Um editor de markdown avançado e histórico de conversa com formatação e backup automático completam a experiência.

## Tecnologias Utilizadas
- **Python 3.11+**
- **PyQt6**: Interface gráfica moderna e responsiva.
- **qasync**: Operações assíncronas para respostas em tempo real.
- **markdown2**: Formatação de respostas e histórico em markdown.
- Integração com múltiplos provedores de IA para respostas contextualizadas.

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Sistema operacional: Windows/Linux/MacOS

### Passo a Passo de Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/KerubinDev/kerubin.git
   cd kerubin
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o arquivo de configuração `config/kerubin.json` conforme necessário.
4. Execute o programa:
   ```bash
   python main.py
   ```

## Recursos Avançados

### 1. Formatação Rica
- Suporte a markdown completo, gráficos ASCII/Unicode, diagramas Mermaid, e blocos de código.
- Emoticons e símbolos para personalizar ainda mais as respostas e o histórico.

### 2. Gerenciamento de Conversas
- Salvamento automático, nomeação inteligente e backup do histórico.
- Configurações para ajustar parâmetros de IA como modelo, tokens e temperatura.

### 3. Personalização de Configurações
- Parâmetros ajustáveis para resposta, contexto e limite de tokens, adaptáveis de acordo com as necessidades do usuário.

## Requisitos do Sistema
- **Sistema Operacional**: Windows/Linux/MacOS
- **Memória RAM**: Mínimo de 4GB
- **Conexão com Internet**

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests. Para contribuições maiores, por favor, entre em contato e discuta suas ideias antes.

## Licença
Distribuído sob a Licença Apache 2.0. Veja `LICENSE` para mais informações.
