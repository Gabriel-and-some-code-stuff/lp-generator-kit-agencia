import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const VerticalFeatures = () => (
  <Section
    title="Nossos Tratamentos"
    description="Oferecemos soluções completas para a saúde e beleza do seu sorriso."
  >
    {AppConfig.features.map((feature, index) => (
      <VerticalFeatureRow
        key={index}
        title={feature.title}
        description={feature.description}
        image={feature.image}
        imageAlt={feature.imageAlt}
        reverse={feature.reverse}
      />
    ))}
  </Section>
);

export { VerticalFeatures };
