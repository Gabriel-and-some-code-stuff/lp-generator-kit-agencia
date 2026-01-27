import Link from 'next/link';

import { Background } from '../background/Background';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Hero = () => {
  const config = AppConfig as any;
  const hero = config?.hero || {};

  return (
    <Background color="bg-white relative">
      {/* Navbar Overlay */}
      <Section yPadding="py-6">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li>
            <Link
              href="/"
              className="text-sm font-semibold text-gray-700 transition-colors hover:text-primary-600"
            >
              HOME
            </Link>
          </li>
          <li>
            <Link
              href="/about"
              className="text-sm font-semibold text-gray-700 transition-colors hover:text-primary-600"
            >
              SOBRE NÓS
            </Link>
          </li>
          <li>
            <Link
              href={hero.buttonLink || '#'}
              className="rounded-md bg-primary-600 px-6 py-3 text-sm font-bold text-white shadow-md transition-all hover:bg-primary-700 hover:shadow-lg"
            >
              {hero.button || 'SOLICITAR COTAÇÃO'}
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      {/* Hero Content - Estilo Corporativo Dividido */}
      <div className="relative overflow-hidden bg-gray-50 pb-24 pt-16 lg:pt-32">
        <div className="mx-auto max-w-screen-xl px-4 sm:px-6">
          <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:items-center">
            {/* Coluna Texto */}
            <div className="relative z-10">
              {hero.highlight && (
                <div className="mb-6 inline-block rounded-full bg-primary-100 px-4 py-1.5">
                  <span className="text-xs font-bold uppercase tracking-wider text-primary-700">
                    {hero.highlight}
                  </span>
                </div>
              )}

              <h1 className="mb-6 text-4xl font-extrabold leading-tight text-gray-900 sm:text-5xl lg:text-6xl">
                {hero.title}
              </h1>

              <p className="mb-8 text-lg leading-relaxed text-gray-600 sm:text-xl">
                {hero.description}
              </p>

              <div className="flex flex-col gap-4 sm:flex-row">
                <Link href={hero.buttonLink || '#'}>
                  <div className="inline-flex cursor-pointer items-center justify-center rounded-lg bg-primary-600 px-8 py-4 text-base font-bold text-white transition-all hover:bg-primary-700 hover:shadow-lg">
                    {hero.button || 'Começar Agora'}
                  </div>
                </Link>
                <Link href="/services">
                  <div className="inline-flex cursor-pointer items-center justify-center rounded-lg border-2 border-gray-200 bg-transparent px-8 py-4 text-base font-bold text-gray-700 transition-all hover:border-gray-300 hover:bg-gray-50">
                    Nossos Serviços
                  </div>
                </Link>
              </div>

              {/* Trust Indicator simples */}
              <div className="mt-10 flex items-center gap-4 text-sm font-medium text-gray-500">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      className="size-8 rounded-full border-2 border-white bg-gray-300"
                    />
                  ))}
                </div>
                <p>Junte-se a mais de 15.000 clientes satisfeitos.</p>
              </div>
            </div>

            {/* Coluna Imagem - Estilo Card Flutuante */}
            <div className="relative lg:ml-10">
              <div className="relative rounded-2xl bg-white p-2 shadow-2xl shadow-primary-900/10">
                <div className="aspect-[4/3] overflow-hidden rounded-xl bg-gray-200">
                  <img
                    src={hero.image}
                    alt="Hero"
                    className="size-full object-cover"
                  />
                </div>

                {/* Floating Badge (Estilo Qualitas 'Accuracy') */}
                <div className="absolute -bottom-6 -left-6 hidden rounded-lg bg-white p-6 shadow-xl lg:block">
                  <div className="flex items-center gap-4">
                    <div className="flex size-12 items-center justify-center rounded-full bg-green-100 text-green-600">
                      <svg
                        className="size-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                    <div>
                      <p className="text-sm font-bold text-gray-900">
                        99.9% Precisão
                      </p>
                      <p className="text-xs text-gray-500">
                        Garantia de conformidade
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Decorative Blob */}
              <div className="absolute -right-12 -top-12 -z-10 size-64 rounded-full bg-primary-100 opacity-50 blur-3xl" />
            </div>
          </div>
        </div>
      </div>
    </Background>
  );
};

export { Hero };
