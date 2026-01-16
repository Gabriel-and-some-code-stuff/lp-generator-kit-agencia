import Link from 'next/link';

import { Button } from '../button/Button';
import { CTABanner } from '../cta/CTABanner';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Banner = () => (
  <Section>
    <CTABanner
      title={AppConfig.cta.title}
      subtitle={AppConfig.cta.subtitle}
      button={
        <Link href={AppConfig.cta.link}>
          <Button>{AppConfig.cta.button}</Button>
        </Link>
      }
    />
  </Section>
);

export { Banner };
