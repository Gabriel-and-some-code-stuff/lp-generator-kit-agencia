export const AppConfig = {
  site_name: 'Nome da Empresa',
  title: 'Título da Landing Page | Promessa Principal',
  description:
    'Descrição curta para SEO (meta description) focada em conversão e autoridade.',
  locale: 'pt-br',

  hero: {
    title: 'Transforme a vida do seu',
    highlight: 'cliente ideal.',
    description:
      'Uma descrição persuasiva que aborda a dor principal do cliente e apresenta a sua solução como a melhor alternativa do mercado.',
    button: 'Chamada para Ação',
    buttonLink: '#',
  },

  features: [
    {
      title: 'Diferencial ou Serviço 1',
      description:
        'Explicação detalhada sobre como este serviço resolve um problema específico do cliente de forma eficiente.',
      image: '/assets/images/feature.svg',
      imageAlt: 'Imagem ilustrativa do serviço 1',
      reverse: false,
    },
    {
      title: 'Diferencial ou Serviço 2',
      description:
        'Destaque para a tecnologia, metodologia ou benefício exclusivo que sua empresa oferece neste ponto.',
      image: '/assets/images/feature2.svg',
      imageAlt: 'Imagem ilustrativa do serviço 2',
      reverse: true,
    },
    {
      title: 'Diferencial ou Serviço 3',
      description:
        'Prova social ou garantia de qualidade que elimina o risco e aumenta a confiança do comprador.',
      image: '/assets/images/feature3.svg',
      imageAlt: 'Imagem ilustrativa do serviço 3',
      reverse: false,
    },
  ],

  cta: {
    title: 'Pronto para dar o próximo passo?',
    subtitle:
      'Entre em contato hoje mesmo e descubra como podemos ajudar você a alcançar seus objetivos.',
    button: 'Falar com Especialista',
    link: '#',
  },

  footer: {
    company_name: 'Nome da Empresa',
    contacts: [
      'Endereço: Rua Exemplo, 123 - Cidade/UF',
      'Telefone: (11) 99999-9999',
      'Email: contato@empresa.com.br',
    ],
  },
};
