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
    <Background color="bg-white">
      <Section yPadding="py-8">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li>
            <Link
              href="/"
              className="text-sm font-medium transition-colors hover:text-gray-600"
            >
              INÍCIO
            </Link>
          </li>
          <li>
            <Link
              href={hero.buttonLink || '#'}
              className="border-b-2 border-black pb-1 text-sm font-bold transition-all hover:border-gray-400"
            >
              {hero.button || 'CONTATO'} ↗
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      <Section yPadding="pt-24 pb-32">
        <div className="grid grid-cols-1 items-start gap-12 lg:grid-cols-12">
          {/* Coluna de Texto (Dominante) */}
          <div className="flex flex-col justify-center lg:col-span-8">
            {/* Label estilo "Ficha Técnica" */}
            <div className="swiss-label mb-6">
              {hero.highlight || 'DESTAQUE'} — 01
            </div>

            <h1 className="sm:text-7xl lg:text-8xl mb-10 text-6xl font-bold leading-[0.95] tracking-tighter text-black">
              {hero.title || 'Título Principal'}
            </h1>

            <div className="grid max-w-2xl grid-cols-1 gap-8 border-t border-gray-200 pt-8 sm:grid-cols-2">
              <p className="text-lg leading-relaxed text-gray-600">
                {hero.description ||
                  'Descrição focada na solução racional do problema.'}
              </p>
              <div className="flex items-start">
                <Link href={hero.buttonLink || '#'}>
                  <div className="group cursor-pointer">
                    <div className="flex size-16 items-center justify-center rounded-full bg-black text-white transition-transform duration-300 group-hover:scale-110">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="size-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 14l-7 7m0 0l-7-7m7 7V3"
                        />
                      </svg>
                    </div>
                    <span className="mt-3 block text-sm font-bold uppercase tracking-wide group-hover:underline">
                      {hero.button || 'Ver Soluções'}
                    </span>
                  </div>
                </Link>
              </div>
            </div>
          </div>

          {/* Coluna de Imagem (Funcional) */}
          <div className="relative mt-12 lg:col-span-4 lg:mt-0">
            {/* Aspect Ratio vertical, estilo editorial */}
            <div className="relative aspect-[3/4] overflow-hidden bg-gray-100">
              <img
                src={
                  hero.image ||
                  'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80'
                }
                alt="Hero"
                className="size-full object-cover grayscale transition-all duration-700 ease-out hover:grayscale-0"
              />
            </div>
            {/* Caption estilo museu */}
            <div className="mt-2 flex items-center justify-between font-mono text-[10px] uppercase text-gray-400">
              <span>Fig. 01</span>
              <span>Visualização do Conceito</span>
            </div>
          </div>
        </div>
      </Section>
    </Background>
  );
};

export { Hero };
