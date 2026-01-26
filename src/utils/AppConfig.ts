// Este arquivo será sobrescrito pela IA, mas aqui está a estrutura ideal
export const AppConfig = {
  site_name: 'Landing Page Generator',
  title: 'Título Otimizado | Promessa',
  description: 'Descrição persuasiva para SEO.',
  locale: 'pt-br',
  primary_color: '#0ea5e9', // Importante para o Tailwind saber a cor base

  hero: {
    title: 'Transforme Visitantes em Clientes',
    highlight: 'Resultados',
    description:
      'Uma descrição focada na dor do cliente e como sua solução resolve isso de forma única.',
    button: 'Agendar Demonstração',
    buttonLink: '#',
    image:
      'https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
  },

  features: [
    {
      title: 'Benefício Principal 1',
      description:
        'Explicação de como esse recurso economiza tempo ou dinheiro.',
      image:
        'https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80',
      imageAlt: 'Benefício 1',
      reverse: false,
    },
    {
      title: 'Benefício Principal 2',
      description:
        'Explicação de como esse recurso traz segurança ou eficiência.',
      image:
        'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
      imageAlt: 'Benefício 2',
      reverse: true,
    },
  ],

  // Nova seção para Prova Social (Essencial para High Converting)
  socialProof: {
    title: 'Confiança de líderes de mercado',
    logos: [], // IA pode preencher ou deixamos vazio
  },

  cta: {
    title: 'Pronto para escalar seus resultados?',
    subtitle:
      'Junte-se a mais de 500 empresas que transformaram seus negócios.',
    button: 'Falar com Consultor',
    link: '#',
  },

  footer: {
    company_name: 'Minha Empresa',
    contacts: ['contato@empresa.com', '(11) 99999-9999'],
  },
};
