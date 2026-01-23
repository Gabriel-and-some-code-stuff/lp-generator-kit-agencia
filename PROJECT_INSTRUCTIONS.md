# PROJECT_INSTRUCTIONS

## Arquitetura do Gerador de Landing Pages  
**Edição Local com Ollama e Selenium**

Automação completa para prospecção e criação de Landing Pages utilizando **Inteligência Artificial Local (Ollama)** e **Scraping Dinâmico (Selenium)**.

O sistema analisa sites existentes, extrai conteúdo relevante, identifica automaticamente o nicho de mercado e gera Landing Pages otimizadas para conversão **sem custos de API**, além de produzir mensagens de abordagem prontas para WhatsApp.

---

## Visão Geral do Fluxo de Dados

```mermaid
graph TD
    A[Planilha CSV] -->|Lê URL e Nome| B(Agente Python)
    B -->|Selenium + ChromeDriver| C{Scraping Dinâmico}
    C -->|HTML Limpo + Imagens| D[Ollama (Llama 3)]
    I[AGENT_INSTRUCTIONS.md] -->|Prompt do Sistema (Nichos e Ganchos)| D
    D -->|Raciocínio: Identifica Nicho e Gera Conteúdo| E[JSON Config + Mensagem WhatsApp]
    E -->|Atualiza AppConfig.ts| F[Build & Test]
    F -->|Sucesso| G[Deploy Vercel]
    G -->|Retorna URL| H[Planilha CSV (Output)]
    E -->|Mensagem de Abordagem| H
```

---

## Componentes do Sistema

### 1. Entrada de Dados (CSV)

**Função**  
Fonte da verdade para toda a prospecção.

**Estrutura da Planilha**

- Coluna A: Nome do Cliente  
- Coluna C: URL do Site Atual (para análise)  
- Coluna D: URL da Landing Page Gerada (output automático)  
- Coluna E: Mensagem de Abordagem WhatsApp (output automático)

---

### 2. O Agente (Orquestrador em Python)

**Bibliotecas Utilizadas**

- pandas  
- selenium  
- requests (API local do Ollama)  
- beautifulsoup4  
- python-dotenv  

**Responsabilidades**

- Lê cada linha da planilha `clientes.csv`
- Acessa o site do cliente via navegador headless usando Selenium
- Extrai e limpa o HTML, mantendo apenas conteúdo relevante
- Envia o conteúdo limpo junto do `AGENT_INSTRUCTIONS.md` para o Ollama local
- Executa raciocínio estratégico com IA:
  - Identificação automática de nicho
  - Seleção de ganchos de conversão
  - Geração do JSON de configuração da Landing Page
  - Criação da mensagem de abordagem para WhatsApp
- Atualiza automaticamente:
  - `src/utils/AppConfig.ts`
  - `tailwind.config.js` (cor primária)
- Executa:
  - `npm run format`
  - Deploy via Vercel CLI
- Salva a URL final da LP e a mensagem de WhatsApp na planilha
- Exibe a mensagem pronta no terminal
- Opcionalmente envia a mensagem via Z-API (se configurado)

---

### 3. Inteligência Artificial Local (Ollama)

**Software**  
Ollama rodando localmente (`localhost:11434`)

**Modelo Sugerido**  
`llama3`

**Vantagens**

- Custo zero de API
- Privacidade total dos dados
- Baixa latência local
- Controle completo de prompts

---

### 4. Estratégia de Nicho (Prompt)

O arquivo `AGENT_INSTRUCTIONS.md` define as regras estratégicas de adaptação da Landing Page para diferentes mercados, como:

- Saúde e Estética  
- Direito e Consultoria  
- Engenharia e Imóveis  
- Serviços Industriais (B2B)  
- Educação  

Esse arquivo funciona como **prompt de sistema**, garantindo consistência de copy, estrutura e foco em conversão.

---

## Pré-requisitos

- Ollama instalado e rodando com o modelo `llama3`
- Google Chrome instalado
- ChromeDriver compatível
- Vercel CLI autenticado
- Node.js e npm configurados
- Python **3.10 ou superior**

---

Este projeto foi pensado para **escala, automação e soberania tecnológica**, eliminando dependência de APIs externas e permitindo geração massiva de Landing Pages com alto nível de personalização.
