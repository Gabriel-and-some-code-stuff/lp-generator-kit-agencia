import Link from 'next/link';

import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Banner = () => {
  const config = AppConfig as any;
  const cta = config?.cta || {};

  if (!cta.title && !cta.button) {
    return null;
  }

  return (
    <Section yPadding="py-24">
      <div className="relative overflow-hidden rounded-2xl bg-gray-900 px-8 py-16 text-center shadow-2xl shadow-gray-900/20 md:px-16 md:py-20 lg:text-left">
        <div className="absolute right-0 top-0 -mr-16 -mt-16 size-64 rounded-full bg-primary-500 opacity-10 blur-3xl" />
        <div className="absolute bottom-0 left-0 -mb-16 -ml-16 size-64 rounded-full bg-primary-500 opacity-10 blur-3xl" />

        <div className="relative z-10 mx-auto flex max-w-5xl flex-col items-center justify-between gap-10 lg:flex-row">
          <div className="max-w-2xl">
            <h2 className="mb-4 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              {cta.title || 'Pronto para começar?'}
            </h2>
            <p className="text-lg leading-relaxed text-gray-300 opacity-90">
              {cta.subtitle || 'Entre em contato hoje mesmo.'}
            </p>
          </div>

          <div className="flex shrink-0 flex-col gap-4 sm:flex-row">
            <Link href={cta.link || '#'}>
              <div className="inline-block cursor-pointer rounded-md bg-white px-10 py-4 text-center text-lg font-bold text-gray-900 transition-all hover:bg-gray-100 hover:shadow-lg">
                {cta.button || 'Fale Conosco'}
              </div>
            </Link>
          </div>
        </div>
      </div>
    </Section>
  );
};

export { Banner };
