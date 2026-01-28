import Link from 'next/link';

import { Button } from '../button/Button';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const SoftCTA = () => {
  const { cta } = AppConfig as any;

  return (
    <Section yPadding="py-20" className="bg-gray-50 text-center">
      <h2 className="mb-6 text-3xl font-bold text-gray-900">{cta.title}</h2>
      <p className="mx-auto mb-8 max-w-2xl text-lg text-gray-600">
        {cta.subtitle}
      </p>
      <Link href={cta.link || '#'}>
        <Button>{cta.button}</Button>
      </Link>
    </Section>
  );
};

export { SoftCTA };
