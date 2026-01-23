import Link from 'next/link';

import { Background } from '../background/Background';
import { Button } from '../button/Button';
import { HeroOneButton } from '../hero/HeroOneButton';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Hero = () => {
  // Garante valores padrão caso a IA falhe em gerar algum campo
  const heroConfig = {
    title: AppConfig.hero?.title || 'Título Padrão',
    highlight: AppConfig.hero?.highlight || 'Destaque',
    description:
      AppConfig.hero?.description || 'Descrição padrão do site gerado.',
    button: AppConfig.hero?.button || 'Saiba Mais',
    buttonLink: AppConfig.hero?.buttonLink || '#', // Fallback seguro
  };

  return (
    <Background color="bg-gray-100">
      <Section yPadding="py-6">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li>
            <Link href="/">Home</Link>
          </li>
          <li>
            {/* Proteção contra undefined */}
            <Link href={heroConfig.buttonLink}>{heroConfig.button}</Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      <Section yPadding="pt-20 pb-32">
        <HeroOneButton
          title={
            <>
              {heroConfig.title}{' '}
              <span className="text-primary-500">{heroConfig.highlight}</span>
            </>
          }
          description={heroConfig.description}
          button={
            <Link href={heroConfig.buttonLink}>
              <Button xl>{heroConfig.button}</Button>
            </Link>
          }
        />
      </Section>
    </Background>
  );
};

export { Hero };
