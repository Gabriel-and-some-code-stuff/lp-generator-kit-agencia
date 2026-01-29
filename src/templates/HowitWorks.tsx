import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const HowItWorks = () => {
  const { howItWorks } = AppConfig as any;
  if (!howItWorks) return null;

  return (
    <Section
      title={howItWorks.title}
      yPadding="py-16 md:py-20"
      className="bg-gray-50/50"
    >
      <div className="mx-auto max-w-6xl">
        {/* MUDANÇA: Usando Flex com justify-center para garantir centralização independente da quantidade */}
        <div className="flex flex-wrap justify-center gap-8 lg:gap-12">
          {howItWorks.steps.map((step: any, index: number) => (
            <div
              key={index}
              className="relative flex w-full max-w-xs flex-col items-center p-4 text-center"
            >
              {/* Conector horizontal removido para simplificar o layout flexível e evitar quebras */}

              <div className="z-10 mb-6 flex size-16 items-center justify-center rounded-2xl border border-gray-100 bg-white text-xl font-bold text-primary-600 shadow-sm transition-transform hover:scale-110">
                {index + 1}
              </div>

              <h3 className="mb-3 text-lg font-bold text-gray-900">
                {step.title}
              </h3>

              <p className="text-sm leading-relaxed text-gray-500">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </Section>
  );
};

export { HowItWorks };
