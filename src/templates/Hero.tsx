import Link from 'next/link';

import { Button } from '../button/Button';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Hero = () => {
  const config = AppConfig as any;
  const hero = config?.hero || {};

  return (
    <div className="relative overflow-hidden bg-white">
      {/* Background mais neutro */}
      <div className="absolute left-1/2 top-0 -z-10 ml-[-40%] h-[700px] w-[200%] rounded-b-[100%] bg-gray-50/60 opacity-60" />

      <NavbarTwoColumns logo={<Logo />}>
        <li>
          <Link
            href="/"
            className="text-gray-600 transition-colors hover:text-primary-600"
          >
            Início
          </Link>
        </li>
        <li>
          <Link
            href="/#services"
            className="text-gray-600 transition-colors hover:text-primary-600"
          >
            Soluções
          </Link>
        </li>
        <li>
          <Link href={hero.buttonLink || '#'}>
            <div className="rounded-lg bg-gray-900 px-5 py-2 text-sm font-semibold text-white transition-all hover:bg-gray-800 hover:shadow-md">
              Contato
            </div>
          </Link>
        </li>
      </NavbarTwoColumns>

      <Section yPadding="pt-32 pb-16 md:pt-40 md:pb-20">
        {' '}
        {/* Ajustado padding top para compensar navbar maior */}
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <div className="flex flex-col items-center text-center lg:items-start lg:text-left">
            {hero.highlight && (
              <div className="mb-6 inline-flex items-center rounded-full border border-primary-100 bg-white px-3 py-1 text-xs font-bold uppercase tracking-widest text-primary-700 shadow-sm">
                {hero.highlight}
              </div>
            )}

            <h1 className="mb-6 text-4xl font-extrabold leading-tight tracking-tight text-gray-900 md:text-5xl lg:text-6xl">
              {hero.title}
            </h1>

            <p className="mb-8 max-w-xl text-lg leading-relaxed text-gray-600 md:text-xl">
              {hero.description}
            </p>

            <div className="flex w-full flex-col gap-4 sm:flex-row sm:justify-center lg:justify-start">
              <Link href={hero.buttonLink || '#'}>
                <Button xl>{hero.button || 'Saiba Mais'}</Button>
              </Link>
              {hero.secondaryButton && (
                <div className="flex cursor-pointer items-center justify-center rounded-lg px-6 py-3 text-base font-semibold text-gray-600 transition-colors hover:text-primary-600">
                  {hero.secondaryButton}
                </div>
              )}
            </div>

            <div className="mt-8 flex items-center gap-4 text-sm font-medium text-gray-500">
              <div className="flex -space-x-2">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="size-8 rounded-full border-2 border-white bg-gray-100"
                  />
                ))}
              </div>
              <p>Junte-se a clientes satisfeitos</p>
            </div>
          </div>

          <div className="relative mx-auto w-full max-w-lg lg:max-w-none">
            <div className="relative overflow-hidden rounded-2xl bg-gray-100 shadow-xl ring-1 ring-gray-900/5">
              {hero.image ? (
                <img
                  src={hero.image}
                  alt={hero.title}
                  className="aspect-[4/3] w-full object-cover"
                />
              ) : (
                <div className="flex aspect-[4/3] w-full items-center justify-center bg-gray-50 text-gray-400">
                  <span className="text-lg">Imagem Principal</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </Section>
    </div>
  );
};

export { Hero };
