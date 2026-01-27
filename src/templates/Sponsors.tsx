import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Sponsors = () => {
  const config = AppConfig as any;
  // Fallback seguro se não houver logotipos definidos
  const logos = config?.socialProof?.logos || [];

  return (
    <div className="border-b border-gray-100 bg-white">
      <Section yPadding="py-10">
        <div className="flex flex-col items-center gap-6 lg:flex-row lg:justify-between">
          <div className="text-center lg:text-left">
            <p className="text-sm font-semibold uppercase tracking-wider text-gray-400">
              Confiado por grandes empresas
            </p>
          </div>

          {/* Área de Logos ou Stats (adaptável) */}
          <div className="flex flex-wrap justify-center gap-8 lg:justify-end lg:gap-12">
            {logos.length > 0 ? (
              logos.map((logoUrl: string, index: number) => (
                <img
                  key={index}
                  src={logoUrl}
                  alt={`Partner ${index}`}
                  className="h-8 w-auto opacity-40 grayscale transition-all duration-300 hover:opacity-100 hover:grayscale-0"
                />
              ))
            ) : (
              // Placeholder estilizado se não houver logos no config
              <>
                {[
                  'Global Corp',
                  'Nexus Finance',
                  'Stratos Tech',
                  'Acme Co',
                ].map((name, i) => (
                  <span
                    key={i}
                    className="text-xl font-bold text-gray-300 grayscale hover:text-gray-500"
                  >
                    {name}
                  </span>
                ))}
              </>
            )}
          </div>
        </div>
      </Section>
    </div>
  );
};

export { Sponsors };
