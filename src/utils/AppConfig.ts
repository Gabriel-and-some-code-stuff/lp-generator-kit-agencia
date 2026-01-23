export const AppConfig = {
  site_name: 'Landing Page Generator',
  title: 'Título do Site | Promessa',
  description: 'Descrição padrão para SEO.',
  locale: 'pt-br',

  hero: {
    title: 'Sua Promessa Principal',
    highlight: 'Destaque',
    description: 'Descrição persuasiva do seu produto ou serviço.',
    button: 'Começar Agora',
    buttonLink: '#',
  },

  features: [
    {
      title: 'Benefício 1',
      description: 'Descrição detalhada do benefício.',
      image: '/assets/images/feature.svg',
      imageAlt: 'Imagem 1',
      reverse: false,
    },
    {
      title: 'Benefício 2',
      description: 'Descrição detalhada do benefício.',
      image: '/assets/images/feature2.svg',
      imageAlt: 'Imagem 2',
      reverse: true,
    },
  ],

  cta: {
    title: 'Chamada para Ação Final',
    subtitle: 'Texto de apoio.',
    button: 'Clique Aqui',
    link: '#',
  },

  footer: {
    company_name: 'Nome da Empresa',
    contacts: ['Endereço da Empresa', '(11) 99999-9999', 'contato@empresa.com'],
  },
};
