// Este arquivo funciona como interface.
// O Agente deve gerar o conteúdo EXATAMENTE respeitando esta estrutura.

export const AppConfig = {
  site_name: 'Nome da Empresa',
  title: 'Título Otimizado para SEO | Promessa',
  description: 'Descrição persuasiva para SEO e compartilhamento social.',
  locale: 'pt-br',

  hero: {
    title: 'Headline Impactante',
    highlight: 'Destaque em Cor',
    description:
      'Subtítulo que resolve uma dor específica e convida para ação.',
    button: 'Texto do CTA',
    buttonLink: '#', // Link para WhatsApp ou Formulário
  },

  features: [
    {
      title: 'Benefício 1',
      description: 'Como isso resolve a vida do cliente.',
      image: '/assets/images/feature.svg', // URL Externa ou local
      imageAlt: 'Descrição da imagem',
      reverse: false,
    },
    {
      title: 'Benefício 2',
      description: 'Descrição focada em autoridade e confiança.',
      image: '/assets/images/feature2.svg',
      imageAlt: 'Descrição da imagem',
      reverse: true,
    },
  ],

  cta: {
    title: 'Chamada Final para Ação',
    subtitle: 'Remoção de objeção final (ex: Orçamento sem compromisso).',
    button: 'Texto do Botão Final',
    link: '#',
  },

  footer: {
    company_name: 'Nome da Empresa',
    contacts: ['Endereço ou Cidade', 'Telefone / WhatsApp', 'Email'],
  },
};
