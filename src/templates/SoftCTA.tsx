import Link from 'next/link';

import { Button } from '../button/Button';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const SoftCTA = () => {
  const { cta } = AppConfig as any;

  return (
    <Section yPadding="py-20" className="bg-white text-center">
      <div className="shadow-soft mx-auto max-w-4xl rounded-3xl border border-gray-100 bg-gray-50 px-6 py-16 md:px-12 md:py-20">
        <h2 className="mb-6 text-3xl font-extrabold text-gray-900 md:text-4xl">
          {cta.title}
        </h2>
        <p className="mx-auto mb-10 max-w-2xl text-xl text-gray-600">
          {cta.subtitle}
        </p>
        <Link href={cta.link || '#'}>
          <Button xl>{cta.button}</Button>
        </Link>
      </div>
    </Section>
  );
};

export { SoftCTA };
