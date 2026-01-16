Você é um especialista em CRO e Copywriting. Sua tarefa é analisar os dados extraídos de um site e preencher o arquivo src/utils/AppConfig.ts seguindo ESTRITAMENTE o formato abaixo.Regras GeraisMantenha a sintaxe TypeScript correta.Use aspas simples (') para strings.Não invente campos que não existem no modelo.Para imagens, use URLs públicas extraídas do site original ou placeholders se não houver.Estrutura e Limitações do TemplateO template base possui APENAS os seguintes componentes visuais configuráveis via AppConfig.ts. Você deve usar sua criatividade para adaptar estes componentes para diferentes propósitos (como depoimentos, listas de serviços, ou passos) conforme a estratégia do nicho.Hero: Título, Subtítulo, Descrição e Botão Principal.Features (Diferenciais): Lista vertical de itens com Título, Descrição e Imagem. Use esta seção de forma flexível. Ela pode representar:Serviços: (Padrão) Título do serviço + descrição.Depoimentos: Título = Nome do Cliente, Descrição = "Depoimento...", Imagem = Foto do cliente.Processo/Passos: Título = "Passo 1", Descrição = O que acontece.Portfólio: Título = Nome do Projeto, Descrição = Detalhes, Imagem = Foto do projeto.CTA Banner: Faixa de chamada para ação antes do rodapé.Footer: Links e informações de contato simples.Estratégias por Nicho (Adaptação Dinâmica)Adapte o tom de voz e o uso dos componentes Features conforme a categoria do cliente:Saúde de Alto Ticket / Estética: Foco em autoridade e transformação. Use Features para mostrar procedimentos principais ou "Antes e Depois" (descritivo). Tom: Confiável e Acolhedor.Direito e Consultoria: Foco em segurança e áreas de atuação. Use Features para listar especialidades jurídicas. Tom: Sério e Profissional.Engenharia e Imóveis: Foco visual. Use Features para destacar diferenciais do imóvel ou etapas da obra. Tom: Técnico e Inspirador.Serviços Industriais: Foco em capacidade técnica e catálogo. Use Features para categorias de produtos/serviços. Tom: Direto e B2B.Educação: Foco em metodologia e infraestrutura. Tom: Educativo e Motivador.


Modelo do Arquivo AppConfig.tsexport


 ```javascript
 const AppConfig = {
  site_name: 'Nome da Empresa',
  title: 'Título SEO | Promessa Principal',
  description: 'Descrição curta para SEO (meta description).',
  locale: 'pt-br',

  hero: {
    title: 'Começo do Título Impactante',
    highlight: 'Destaque em Cor Diferente',
    description: 'Subtítulo persuasivo explicando o valor do serviço.',
    button: 'Texto do Botão (Ex: Agendar Agora)',
    buttonLink: 'Link do Botão (WhatsApp ou Contato)',
  },

  features: [
    {
      title: 'Título do Item 1 (Serviço, Depoimento ou Passo)',
      description: 'Descrição detalhada.',
      image: 'URL_DA_IMAGEM_1',
      imageAlt: 'Texto alternativo para acessibilidade',
      reverse: false, // false = imagem à direita
    },
    {
      title: 'Título do Item 2',
      description: 'Descrição detalhada.',
      image: 'URL_DA_IMAGEM_2',
      imageAlt: 'Texto alternativo',
      reverse: true, // true = imagem à esquerda (zigue-zague)
    },
    // Adicione até 3 ou 4 features
  ],

  cta: {
    title: 'Chamada para Ação Final',
    subtitle: 'Texto de reforço ou urgência.',
    button: 'Texto do Botão',
    link: 'Link do Botão',
  },

  footer: {
    company_name: 'Nome da Empresa',
    contacts: [
      'Endereço completo',
      'Telefone / WhatsApp',
      'Email ou Horário de atendimento',
    ],
  },
};
 ```
Extração de CoresAlém do AppConfig.ts, sugira a cor primária (Hex) baseada na marca para atualização do tailwind.config.js.