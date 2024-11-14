# 🌐 **Kerubin - Assistente Virtual Inteligente**

### **Visão Geral**
Kerubin é um assistente virtual de código aberto desenvolvido em Python, utilizando modelos avançados de linguagem para fornecer respostas contextuais e interativas. Com uma interface gráfica moderna e intuitiva, construída com PyQt6, o Kerubin se destaca pela eficiência e acessibilidade.

---

## 🛠️ **Arquitetura do Sistema**

1. **🖥️ Interface do Usuário** (`src/interface/janela_principal.py`)
   - Tema escuro para conforto visual 👓
   - Barra lateral retrátil para navegação simplificada
   - Editor de texto com suporte a markdown 📝
   - Histórico de conversas com formatação HTML

2. **🧠 Núcleo do Assistente** (`src/assistente/chat_ia.py`)
   - Processamento assíncrono para alta performance 🔄
   - Análise de sentimento e extração de entidades
   - Integração com múltiplos provedores de IA 🔗
   - Aprendizado contínuo baseado em interações

3. **🗄️ Sistema de Memória** (`cerebro/memoria/memoria_ia.py`)
   - Gerenciamento de histórico de conversas
   - Sistema de contexto dinâmico
   - Formatação com markdown e gráficos ASCII 📊
   
4. **📂 Gerenciamento de Sessões** (`src/utils/gerenciador_sessoes.py`)
   - Organização automática de histórico 🗃️
   - Backup e recuperação de dados
   - Limpeza automática de dados antigos

---

## 🚀 **Principais Funcionalidades**

1. **🔍 Processamento de Linguagem Natural**
   - Respostas contextuais ricas, formatadas em markdown.

2. **🧩 Sistema de Memória Contextual**
   - Memória persistente para conversas longas e complexas.

3. **🌈 Interface Gráfica Responsiva**
   - GUI com barra lateral, editor de markdown, e barra de ferramentas interativa.

---

## 💻 **Tecnologias Utilizadas**

| Tecnologia         | Função                                    |
|--------------------|-------------------------------------------|
| **Python 3.11+**   | Linguagem de programação principal        |
| **PyQt6**          | Criação de Interface Gráfica             |
| **qasync**         | Processamento assíncrono                 |
| **markdown2**      | Formatação em markdown                   |
| **Provedores de IA** | Integração com IA para respostas contextuais |

---

## ⚙️ **Instalação e Configuração**

### Passo-a-Passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/kerubin.git
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o arquivo `config/kerubin.json` conforme necessário.
4. Execute o programa:
   ```bash
   python main.py
   ```

---

## 💡 **Recursos Avançados**

1. **📑 Formatação Rica**
   - Suporte completo a markdown, gráficos ASCII e diagramas Mermaid.

2. **🔄 Gerenciamento de Conversas**
   - Salvamento e recuperação automáticos com nomeação inteligente.

3. **🛠️ Personalização**
   - Ajuste de modelos, temperatura e outros parâmetros da IA.

---

## 🔮 **Melhorias Futuras e Possibilidades de Expansão**

### 1. 🌐 Expansão da Memória Longa e Curta
   - **Memória de Contexto Profundo** para recuperação de memórias de longo prazo.
   - **Ponderação de Contexto** para ajustar a carga de informações conforme a importância.

### 2. 🌍 Suporte a Multilinguagem e Tradução Automática
   - Módulos para tradução em tempo real e resposta automática em múltiplos idiomas.

### 3. 🎨 Melhoria na Interface Gráfica
   - Suporte para tema claro e opções de personalização.

### 4. 🔗 Integração com Ferramentas Externas
   - Conectores para APIs como calendários, CRMs e ferramentas de produtividade.

### 5. 🗣️ Aprimoramento do Processamento de Linguagem Natural
   - Análise de sentimento avançada e comandos de voz para feedback sonoro.

### 6. 🔒 Segurança e Privacidade
   - **Criptografia** de conversas e gerenciamento granular de permissões.

### 7. 📊 Ferramentas de Análise e Relatórios
   - Relatórios personalizados com métricas de interação.

---

## 🤝 **Contribuições**

Contribuições são bem-vindas! Para sugerir melhorias, reporte bugs ou envie pull requests. 

---

## 📝 **Licença**
Este projeto está sob a licença Apache 2.0. Consulte o arquivo [LICENSE](LICENSE) para mais informações.
