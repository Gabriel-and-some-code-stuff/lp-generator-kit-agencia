import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const HowItWorks = () => {
  const { howItWorks } = AppConfig as any;
  if (!howItWorks) return null;

  return (
    <Section
      title={howItWorks.title}
      yPadding="py-20 md:py-28"
      className="bg-gray-900 text-white"
    >
      <div className="grid gap-12 md:grid-cols-4">
        {howItWorks.steps.map((step: any, index: number) => (
          <div key={index} className="relative">
            <div className="mb-6 text-5xl font-black text-primary-500 opacity-30">
              {index + 1}
            </div>
            <h3 className="mb-3 text-lg font-bold text-white">{step.title}</h3>
            <p className="leading-relaxed text-gray-400">{step.description}</p>
            {index !== howItWorks.steps.length - 1 && (
              <div className="absolute right-0 top-12 hidden h-0.5 w-1/2 bg-gray-800 md:block lg:w-2/3" />
            )}
          </div>
        ))}
      </div>
    </Section>
  );
};

export { HowItWorks };
