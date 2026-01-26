import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const VerticalFeatures = () => {
  const config = AppConfig as any;
  const features = config?.features || [];

  return (
    <Section
      title="Por que escolher nossa solução?"
      description="Focamos no que realmente importa: resultados consistentes e crescimento sustentável."
    >
      <div className="mt-12 space-y-24">
        {features.map((feature: any, index: number) => (
          <VerticalFeatureRow
            key={index}
            title={feature.title}
            description={feature.description}
            image={feature.image}
            imageAlt={feature.imageAlt}
            reverse={feature.reverse}
          />
        ))}
      </div>
    </Section>
  );
};

export { VerticalFeatures };
