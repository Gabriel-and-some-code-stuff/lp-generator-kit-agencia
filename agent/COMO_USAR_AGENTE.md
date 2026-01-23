# COMO_USAR_AGENTE

## 🤖 Manual de Operação do Agente de Landing Pages (v2.0)

Automação completa para prospecção e criação de Landing Pages utilizando:

- **Ollama** (Inteligência Artificial Local)
- **Selenium** (Scraping Dinâmico)
- **Z-API** (Envio de mensagens via WhatsApp)

Este agente foi projetado para rodar localmente, sem dependência de APIs pagas, permitindo escala, controle e privacidade.

---

## 🛠️ Configuração Inicial

### 1. Requisitos Básicos

- Python **3.10 ou superior**
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome

---

### 2. Instalação de Dependências

No diretório do projeto, execute:

```bash
pip install -r agent/requirements.txt
```

---

### 3. Configuração do Ollama (IA Local)

1. Baixe o Ollama em:
   - https://ollama.com

2. Baixe o modelo recomendado:

```bash
ollama pull llama3
```

3. Inicie o servidor local:

```bash
ollama serve
```

O Ollama ficará disponível em `http://localhost:11434`.

---

### 4. Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
ZAPI_INSTANCE_ID=seu_id
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token
```

Essas variáveis são utilizadas para o envio automático de mensagens via WhatsApp.

---

## 🚀 Execução do Agente

### 1. Criar o Arquivo de Entrada

Na raiz do projeto, crie o arquivo `clientes.csv` com a seguinte estrutura:

- Nome  
- Telefone  
- URL  

Cada linha representa um cliente a ser analisado e processado.

---

### 2. Executar o Agente

Com tudo configurado, execute:

```bash
python agent/agent.py
```

O agente irá:

- Analisar o site do cliente
- Identificar o nicho automaticamente
- Gerar a Landing Page otimizada
- Realizar o deploy
- Criar a mensagem de abordagem para WhatsApp
- Registrar os resultados no CSV

---

Este fluxo foi pensado para **execução simples**, **automação total** e **mínima intervenção humana**, permitindo rodar campanhas de prospecção em escala com consistência.
