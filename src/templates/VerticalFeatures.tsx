import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const VerticalFeatures = () => {
  const config = AppConfig as any;
  const featuresList = config?.features || [];

  if (!featuresList || featuresList.length === 0) {
    return null;
  }

  return (
    <Section
      title={config.featuresTitle || 'Nossos Diferenciais'}
      description={
        config.featuresDescription ||
        'Soluções completas pensadas para o seu negócio.'
      }
      yPadding="py-24 md:py-32"
      className="bg-gray-50"
    >
      <div className="grid grid-cols-1 gap-10 md:grid-cols-2 lg:grid-cols-3 lg:gap-12">
        {featuresList.map((feature: any, index: number) => (
          <VerticalFeatureRow key={index} {...feature} />
        ))}
      </div>
    </Section>
  );
};

export { VerticalFeatures };
