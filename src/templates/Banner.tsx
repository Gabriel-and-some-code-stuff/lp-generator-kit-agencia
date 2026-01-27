import Link from 'next/link';

import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Banner = () => {
  const config = AppConfig as any;
  const cta = config?.cta || {};

  return (
    <Section className="my-16">
      <div className="relative overflow-hidden rounded-2xl bg-primary-900 px-8 py-16 text-center shadow-2xl md:px-12 md:py-20 lg:px-20 lg:text-left">
        {/* Decorative Background Elements */}
        <div className="absolute right-0 top-0 -mr-20 -mt-20 size-80 rounded-full bg-primary-800 opacity-50 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -mb-20 -ml-20 size-80 rounded-full bg-primary-700 opacity-30 blur-3xl"></div>

        <div className="relative z-10 flex flex-col items-center justify-between gap-8 lg:flex-row">
          <div className="max-w-2xl">
            <h2 className="mb-4 text-3xl font-bold tracking-tight text-white md:text-4xl">
              {cta.title || 'Pronto para otimizar sua folha de pagamento?'}
            </h2>
            <p className="text-lg text-primary-100 opacity-90">
              {cta.subtitle ||
                'Entre em contato hoje e descubra como podemos ajudar sua empresa.'}
            </p>
          </div>

          <div className="flex shrink-0 flex-col gap-4 sm:flex-row">
            <Link href={cta.link || '#'}>
              <div className="inline-block cursor-pointer rounded-lg bg-white px-8 py-4 text-center text-base font-bold uppercase tracking-wide text-primary-900 transition-colors hover:bg-gray-50 hover:shadow-lg">
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
