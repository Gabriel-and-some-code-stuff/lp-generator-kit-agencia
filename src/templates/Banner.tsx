import Link from 'next/link';

import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Banner = () => {
  const config = AppConfig as any;
  const cta = config?.cta || {};

  return (
    <Section>
      <div className="bg-black p-16 text-center text-white md:p-24">
        <div className="swiss-label mb-8 text-gray-400">Conclusão — 03</div>

        <h2 className="mx-auto mb-8 max-w-4xl text-4xl font-bold leading-none tracking-tighter md:text-6xl">
          {cta.title || 'Pronto para começar?'}
        </h2>

        <p className="mx-auto mb-12 max-w-xl text-xl font-light text-gray-400">
          {cta.subtitle || 'Entre em contato.'}
        </p>

        <Link href={cta.link || '#'}>
          <div className="inline-block cursor-pointer border border-white px-12 py-4 text-lg font-bold uppercase tracking-widest transition-colors duration-300 hover:bg-white hover:text-black">
            {cta.button || 'Iniciar'}
          </div>
        </Link>
      </div>
    </Section>
  );
};

export { Banner };
