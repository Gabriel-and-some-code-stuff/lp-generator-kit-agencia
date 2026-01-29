import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const HowItWorks = () => {
  const { howItWorks } = AppConfig as any;
  if (!howItWorks) return null;

  return (
    <Section
      title={howItWorks.title}
      yPadding="py-12 md:py-20"
      className="bg-white"
    >
      <div className="mx-auto max-w-4xl">
        <div className="grid gap-6 md:grid-cols-3">
          {howItWorks.steps.map((step: any, index: number) => (
            <div
              key={index}
              className="relative flex flex-col items-center rounded-2xl border border-gray-100 bg-gray-50 p-5 text-center transition-all hover:-translate-y-1 hover:shadow-md"
            >
              {/* Número do Passo */}
              <div className="mb-3 flex size-10 items-center justify-center rounded-full bg-primary-100 text-lg font-bold text-primary-600">
                {index + 1}
              </div>

              <h3 className="mb-2 text-lg font-bold text-gray-900">
                {step.title}
              </h3>

              <p className="text-sm leading-relaxed text-gray-600">
                {step.description}
              </p>

              {/* Seta indicativa para mobile (visual apenas) */}
              {index !== howItWorks.steps.length - 1 && (
                <div className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-gray-300 md:hidden">
                  ↓
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </Section>
  );
};

export { HowItWorks };
