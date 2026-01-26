import Link from 'next/link';

import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Banner = () => {
  const config = AppConfig as any;
  const cta = config?.cta || {};

  return (
    <Section>
      <div className="relative overflow-hidden rounded-3xl bg-gray-900 p-12 text-center shadow-2xl sm:text-left">
        {/* Background Pattern */}
        <div className="absolute right-0 top-0 -mr-20 -mt-20 size-64 rounded-full bg-primary-500 opacity-20 blur-3xl"></div>

        <div className="relative z-10 flex flex-col items-center justify-between gap-8 sm:flex-row">
          <div className="max-w-2xl text-white">
            <h2 className="text-3xl font-bold">{cta.title || 'Título CTA'}</h2>
            <p className="mt-4 text-lg text-gray-300">
              {cta.subtitle || 'Subtítulo CTA'}
            </p>
          </div>

          <div className="whitespace-no-wrap">
            <Link href={cta.link || '#'}>
              <div className="inline-block cursor-pointer rounded-full bg-white px-8 py-4 text-lg font-bold text-gray-900 shadow-lg transition-colors hover:bg-gray-100">
                {cta.button || 'Clique Aqui'}
              </div>
            </Link>
          </div>
        </div>
      </div>
    </Section>
  );
};

export { Banner };
