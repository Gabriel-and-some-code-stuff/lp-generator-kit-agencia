import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const HowItWorks = () => {
  const { howItWorks } = AppConfig as any;
  if (!howItWorks) return null;

  return (
    <Section
      title={howItWorks.title}
      yPadding="py-16 md:py-20" // Reduzido
      className="bg-gray-50/50" // Fundo muito leve para diferenciar sutilmente
    >
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {' '}
          {/* Mudado para até 4 colunas em telas grandes */}
          {howItWorks.steps.map((step: any, index: number) => (
            <div
              key={index}
              className="relative flex flex-col items-center p-4 text-center"
            >
              {/* Conector horizontal para desktop (exceto o último) */}
              {index !== howItWorks.steps.length - 1 && (
                <div className="absolute left-[60%] top-8 -z-10 hidden h-0.5 w-[80%] bg-gray-200 lg:block" />
              )}

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
