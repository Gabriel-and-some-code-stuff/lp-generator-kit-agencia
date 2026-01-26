import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const VerticalFeatures = () => {
  const config = AppConfig as any;

  const sectionTitle = config?.featuresTitle || 'Nossas Soluções';
  const sectionDesc =
    config?.featuresDescription || 'O que oferecemos de melhor para você.';

  const featuresList =
    config?.features && Array.isArray(config.features)
      ? config.features
      : [
          {
            title: 'Serviço de Qualidade',
            description: 'Descrição do serviço oferecido pela empresa.',
            image: '/assets/images/feature.svg',
            imageAlt: 'Feature 1',
            reverse: false,
          },
        ];

  return (
    <Section title={sectionTitle} description={sectionDesc}>
      <div className="flex flex-col gap-y-24">
        {' '}
        {/* Espaçamento vertical generoso */}
        {featuresList.map((feature: any, index: number) => (
          <VerticalFeatureRow
            key={index}
            title={feature.title || 'Título Indefinido'}
            description={feature.description || 'Sem descrição.'}
            image={feature.image || '/assets/images/feature.svg'}
            imageAlt={feature.imageAlt || 'Imagem'}
            reverse={feature.reverse}
            index={index + 1} // Passa índice para numeração suíça
          />
        ))}
      </div>
    </Section>
  );
};

export { VerticalFeatures };
