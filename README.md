# Landing Page Automation Pipeline (Conversion‑First)

Este repositório implementa um **pipeline automatizado de análise, extração e reconstrução de landing pages**, focado em **conversão, CTA e geração de leads** — não em estética superficial. A proposta é simples e agressiva: pegar sites reais (geralmente medianos ou ruins), extrair o que **realmente gera valor de negócio**, e reconstruir uma LP moderna, estruturada e altamente conversiva usando um sistema data‑driven.

O sistema foi desenhado para funcionar com **agentes de IA**, mas com **guard rails claros**, falhas seguras e arquitetura determinística. Nada aparece na tela por acidente. Nada some sem motivo.

---

## Visão Geral da Arquitetura

O projeto é dividido em **três camadas principais**, cada uma com responsabilidades bem definidas:

1. **Extração & Análise (Scraper + Parser)**
2. **Normalização Semântica (JSON intermediário)**
3. **Renderização Determinística (Front‑end React + Configuração)**

A renderização final do site depende exclusivamente da presença de dados válidos no arquivo de configuração central. Isso permite que agentes automatizados **liguem ou desliguem seções inteiras** sem tocar no código de interface.

---

## Fluxo Completo do Sistema

### 1. Coleta da Fonte

O pipeline parte de um site externo (normalmente um site legado, confuso ou mal estruturado). O scraper gera dois artefatos principais:

* `clean_source.html` → HTML limpo, sem scripts irrelevantes, ads ou ruído visual.
* `contexto_para_agente.txt` → Texto normalizado contendo serviços, regiões, claims, diferenciais e pistas semânticas.
* `agent/downloaded_css/` → Diretório com arquivos CSS baixados e salvos pelo scraper (inclui conteúdo inlined e externo). Esses arquivos são fornecidos ao agente para auxiliar na detecção de paleta de cores e tokens visuais.

O objetivo aqui **não é copiar layout**, mas preservar **informação de negócio**.

---

### 2. Análise Semântica

Um agente lê **ambos os arquivos** (`clean_source.html` + `contexto_para_agente.txt`) e executa:

* Identificação de seções implícitas (mesmo que não existam `<section>` claras)
* Extração de serviços, provas, diferenciais, regiões atendidas
* Inferência controlada quando necessário (ex: anos de mercado a partir de datas)

⚠️ Importante: o agente **não deve apagar valor** apenas porque a estrutura HTML é ruim.

---

### 3. Normalização em Configuração

Toda a LP é controlada por **um único arquivo**:

```
src/utils/AppConfig.ts
```

Cada seção do site possui um *guard clause*. Exemplo:

* Se `benefits` não existir → a seção Benefits **não renderiza**
* Se `solution` existir com dados → a seção aparece automaticamente

Isso garante:

* Fail‑safe visual
* Expansão automática por agentes
* Zero acoplamento entre dados e UI

---

## Seções Suportadas

O front‑end suporta, entre outras:

* Hero / Banner
* Base institucional
* Trust / Credibilidade
* Problem (dor)
* Solution / Services
* Benefits
* How It Works / Methodology
* Social Proof (logos, textos)
* Regional Proof (cidades, cobertura)
* FAQ / Objection Crusher
* Soft CTA e Hard CTA
* Contact Form
* Footer

Nenhuma seção é obrigatória. **Dados mandam. UI obedece.**

---

## Por Que Sites “Meia Boca”?

O produto **não faz sentido** em sites excelentes.

Ele existe para:

* Empresas com muita informação valiosa mal organizada
* Negócios com serviços bons, mas comunicação fraca
* Sites cheios de texto, mas sem hierarquia de conversão

A automação serve para **destilar valor**, não para enfeitar mediocridade.

---

## Erros Conhecidos (e Aprendizados)

Casos reais mostraram falhas comuns:

* Logo usado como imagem de Hero
* Serviços ignorados por não estarem em `<ul>`
* Provas regionais removidas por parecerem “texto solto”
* CTAs genéricos repetidos ("Orçamento", "Enviar Mensagem")

Esses erros **não são bugs de código**, mas falhas de **análise semântica do agente**.

---

## Diretrizes para Agentes de IA

Um agente bem‑comportado deve:

* Priorizar densidade de informação relevante
* Reorganizar semanticamente, não truncar
* Inferir com parcimônia e justificar inferências
* Nunca usar logos como heros
* Tratar listas de serviços como ativos centrais
* Variar CTAs conforme contexto e estágio do funil

O objetivo final é **performance**, não minimalismo estéril.

---

## Filosofia do Projeto

* Performance > Estética
* Clareza > Criatividade vazia
* Dados > Opinião
* Arquitetura previsível > UI mágica

Uma landing page boa **não é bonita**.
Ela é **inevitável**.

---

## Status

Pipeline funcional.
Scraper validado.
Front‑end determinístico.
Agentes em iteração.

O sistema está pronto para evolução — desde que a inteligência semântica acompanhe a ambição.
