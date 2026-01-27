import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const VerticalFeatures = () => {
  const config = AppConfig as any;
  const featuresList = config?.features || [];

  return (
    <Section
      title="Nossos Serviços Especializados"
      description="Soluções completas e adaptáveis para simplificar a gestão do seu negócio."
      yPadding="py-20 bg-white"
    >
      {/* Transformando a lista em um Grid estilo Cards (Padrão Qualitas) */}
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
        {featuresList.map((feature: any, index: number) => (
          <VerticalFeatureRow key={index} {...feature} index={index} />
        ))}
      </div>
    </Section>
  );
};

export { VerticalFeatures };
