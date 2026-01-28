import Link from 'next/link';

import { Background } from '../background/Background';
import { Button } from '../button/Button';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Hero = () => {
  const config = AppConfig as any;
  const hero = config?.hero || {};

  return (
    <Background color="bg-white">
      <Section yPadding="py-6">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li>
            <Link
              href="/"
              className="font-medium text-gray-700 hover:text-primary-600"
            >
              Início
            </Link>
          </li>
          <li>
            <Link
              href="/services"
              className="font-medium text-gray-700 hover:text-primary-600"
            >
              Serviços
            </Link>
          </li>
          <li>
            <Link href={hero.buttonLink || '#'}>
              <div className="rounded-md bg-primary-600 px-5 py-2 font-bold text-white hover:bg-primary-700">
                Contato
              </div>
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      <Section yPadding="pt-16 pb-20 md:pt-28 md:pb-32">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div className="max-w-2xl">
            {hero.highlight && (
              <div className="bg-primary-50 mb-6 inline-block rounded-full px-4 py-1.5 text-sm font-bold uppercase tracking-wider text-primary-700">
                {hero.highlight}
              </div>
            )}
            <h1 className="mb-6 text-5xl font-extrabold leading-tight text-gray-900 md:text-6xl">
              {hero.title}
            </h1>
            <p className="mb-8 text-xl leading-relaxed text-gray-600">
              {hero.description}
            </p>
            <div className="flex flex-col gap-4 sm:flex-row">
              <Link href={hero.buttonLink || '#'}>
                <Button xl>{hero.button || 'Começar Agora'}</Button>
              </Link>
              {hero.secondaryButton && (
                <div className="flex cursor-pointer items-center justify-center rounded-md border-2 border-gray-200 bg-transparent px-8 py-3.5 text-lg font-bold text-gray-700 hover:bg-gray-50">
                  {hero.secondaryButton}
                </div>
              )}
            </div>
          </div>
          <div className="relative mx-auto w-full lg:max-w-none">
            <div className="relative overflow-hidden rounded-xl shadow-2xl">
              {hero.image ? (
                <img
                  src={hero.image}
                  alt={hero.title}
                  className="size-full object-cover"
                />
              ) : (
                <div className="flex h-64 w-full items-center justify-center bg-gray-200 text-gray-400">
                  Placeholder
                </div>
              )}
            </div>
          </div>
        </div>
      </Section>
    </Background>
  );
};

export { Hero };
