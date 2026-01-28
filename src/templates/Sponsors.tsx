import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Sponsors = () => {
  const config = AppConfig as any;
  const socialProof = config?.socialProof;
  const logos = socialProof?.logos || [];

  if (!logos || logos.length === 0) {
    return null;
  }

  return (
    <div className="border-b border-gray-100 bg-white">
      <Section yPadding="py-10 md:py-12">
        <div className="flex flex-col items-center justify-center gap-8 lg:flex-row lg:justify-between">
          {socialProof?.title && (
            <p className="text-sm font-bold uppercase tracking-widest text-gray-400">
              {socialProof.title}
            </p>
          )}

          <div className="flex flex-wrap justify-center gap-x-12 gap-y-8 opacity-60 grayscale transition-all duration-500 hover:opacity-100 hover:grayscale-0">
            {logos.map((logoUrl: string, index: number) => (
              <img
                key={index}
                src={logoUrl}
                alt={`Partner ${index + 1}`}
                className="h-8 w-auto object-contain md:h-10"
              />
            ))}
          </div>
        </div>
      </Section>
    </div>
  );
};

export { Sponsors };
