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
      <Section yPadding="py-6">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li>
            <Link href="/">Início</Link>
          </li>
          <li>
            <Link
              href={hero.buttonLink || '#'}
              className="font-bold text-primary-500"
            >
              {hero.button || 'Contato'}
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      <Section yPadding="pt-20 pb-32">
        <div className="flex flex-col items-center gap-12 md:flex-row">
          {/* Texto à Esquerda */}
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-5xl font-extrabold leading-tight tracking-tight text-gray-900">
              {hero.title || 'Título Principal'}
              <span className="block text-primary-500">
                {hero.highlight || ''}
              </span>
            </h1>
            <p className="mx-auto mt-6 max-w-lg text-xl text-gray-500 md:mx-0">
              {hero.description || 'Descrição padrão.'}
            </p>
            <div className="mt-8 flex justify-center md:justify-start">
              <Link href={hero.buttonLink || '#'}>
                <div className="cursor-pointer rounded-lg bg-primary-500 px-8 py-4 text-lg font-bold text-white shadow-lg transition-all hover:-translate-y-1 hover:bg-primary-600">
                  {hero.button || 'Saiba Mais'}
                </div>
              </Link>
            </div>
          </div>

          {/* Imagem Heroica à Direita */}
          <div className="relative w-full flex-1">
            <div className="animate-blob absolute -left-4 top-0 size-72 rounded-full bg-primary-300 opacity-70 mix-blend-multiply blur-xl"></div>
            <div className="animate-blob animation-delay-2000 absolute -right-4 top-0 size-72 rounded-full bg-purple-300 opacity-70 mix-blend-multiply blur-xl"></div>
            <img
              src={hero.image || 'https://via.placeholder.com/600x400'}
              alt="Hero"
              className="relative z-10 w-full rounded-2xl object-cover shadow-2xl transition-transform duration-500 hover:scale-[1.02]"
            />
          </div>
        </div>
      </Section>
    </Background>
  );
};

export { Hero };
