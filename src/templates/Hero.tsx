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
    <Background color="bg-white relative overflow-hidden">
      {/* Elemento decorativo de fundo */}
      <div className="bg-primary-50/50 absolute left-1/2 top-0 ml-[40rem] size-[80rem] -translate-y-1/2 rounded-full blur-3xl" />

      <Section yPadding="py-4 relative z-10">
        <NavbarTwoColumns logo={<Logo xl />}>
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
              Serviços
            </Link>
          </li>
          <li>
            <Link href={hero.buttonLink || '#'}>
              <div className="rounded-full bg-gray-900 px-5 py-2 text-sm font-semibold text-white transition-all hover:bg-gray-800 hover:shadow-lg">
                Contato
              </div>
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      <Section yPadding="pt-10 pb-12 md:pt-16 md:pb-20 relative z-10">
        <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-8">
          <div className="flex flex-col items-center text-center lg:items-start lg:text-left">
            {hero.highlight && (
              <div className="bg-primary-50 mb-4 inline-flex items-center rounded-full border border-primary-100 px-3 py-1 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wide text-primary-700">
                  {hero.highlight}
                </span>
              </div>
            )}
            <h1 className="mb-5 text-4xl font-black leading-tight text-gray-900 md:text-5xl lg:text-6xl">
              {hero.title}
            </h1>
            <p className="mb-6 max-w-xl text-lg leading-relaxed text-gray-500">
              {hero.description}
            </p>
            <div className="flex w-full flex-col gap-3 sm:flex-row sm:justify-center lg:justify-start">
              <Link href={hero.buttonLink || '#'}>
                <Button xl>{hero.button || 'Começar Agora'}</Button>
              </Link>
              {hero.secondaryButton && (
                <div className="flex cursor-pointer items-center justify-center rounded-full border border-gray-200 bg-white px-6 py-3 text-base font-bold text-gray-700 transition-all hover:border-gray-300 hover:bg-gray-50 hover:shadow-sm">
                  {hero.secondaryButton}
                </div>
              )}
            </div>

            <div className="mt-6 flex items-center gap-3 text-xs font-medium text-gray-500">
              <div className="flex -space-x-2">
                <div className="size-6 rounded-full border-2 border-white bg-gray-200"></div>
                <div className="size-6 rounded-full border-2 border-white bg-gray-300"></div>
                <div className="size-6 rounded-full border-2 border-white bg-gray-400"></div>
              </div>
              <p>Junte-se a +100 clientes satisfeitos</p>
            </div>
          </div>

          <div className="relative mx-auto w-full max-w-md lg:max-w-none">
            <div className="relative rounded-2xl bg-gray-100 shadow-xl shadow-primary-900/10 ring-1 ring-gray-900/5">
              {hero.image ? (
                <img
                  src={hero.image}
                  alt={hero.title}
                  className="size-full rounded-2xl object-cover"
                />
              ) : (
                <div className="flex aspect-square w-full items-center justify-center rounded-2xl bg-gray-50 text-gray-300">
                  <svg
                    className="size-16"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
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
