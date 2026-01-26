import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Sponsors = () => {
  const config = AppConfig as any;
  const siteName = config?.site_name || 'Empresa';

  return (
    <Section yPadding="py-12" className="border-y border-gray-100">
      <div className="flex flex-col items-center justify-between gap-8 md:flex-row">
        <div className="min-w-[200px] text-sm font-semibold uppercase tracking-widest text-gray-400">
          Confiado por líderes
        </div>

        <div className="flex w-full flex-wrap justify-center gap-8 opacity-60 transition-opacity duration-500 hover:opacity-100 md:justify-end md:gap-16">
          {/* Placeholder logos estilizados com tipografia. 
            Em um cenário real, seriam SVGs monocromáticos.
          */}
          <span className="text-xl font-bold tracking-tighter text-gray-300">
            GLOBAL CORP
          </span>
          <span className="text-xl font-bold tracking-tighter text-gray-300">
            NEXUS
          </span>
          <span className="text-xl font-bold tracking-tighter text-gray-300">
            STRATOS
          </span>
          <span className="text-xl font-bold uppercase tracking-tighter text-gray-300">
            {siteName}
          </span>
        </div>
      </div>
    </Section>
  );
};

export { Sponsors };
