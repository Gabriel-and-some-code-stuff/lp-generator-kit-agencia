import Link from 'next/link';

import { Background } from '../background/Background';
import { Button } from '../button/Button';
import { HeroOneButton } from '../hero/HeroOneButton';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Hero = () => (
  <Background color="bg-gray-100">
    <Section yPadding="py-6">
      <NavbarTwoColumns logo={<Logo xl />}>
        <li>
          <Link href="/">Home</Link>
        </li>
        <li>
          <Link href={AppConfig.hero.buttonLink}>{AppConfig.hero.button}</Link>
        </li>
      </NavbarTwoColumns>
    </Section>

    <Section yPadding="pt-20 pb-32">
      <HeroOneButton
        title={
          <>
            {AppConfig.hero.title}{' '}
            <span className="text-primary-500">{AppConfig.hero.highlight}</span>
          </>
        }
        description={AppConfig.hero.description}
        button={
          <Link href={AppConfig.hero.buttonLink}>
            <Button xl>{AppConfig.hero.button}</Button>
          </Link>
        }
      />
    </Section>
  </Background>
);

export { Hero };
