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
      {/* Navigation Layer */}
      <Section yPadding="py-6">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li>
            <Link
              href="/"
              className="text-base font-semibold text-gray-700 transition-colors hover:text-primary-600"
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              href={hero.buttonLink || '#'}
              className="text-base font-semibold text-gray-700 transition-colors hover:text-primary-600"
            >
              Services
            </Link>
          </li>
          <li>
            {/* Primary Action in Navbar */}
            <Link href={hero.buttonLink || '#'}>
              <div className="cursor-pointer rounded-md bg-primary-500 px-5 py-2.5 text-sm font-bold text-white shadow-sm transition-all hover:bg-primary-600 hover:shadow-md">
                Get Started
              </div>
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>

      {/* Hero Content Layer */}
      <Section yPadding="pt-16 pb-20 md:pt-28 md:pb-32">
        <div className="grid grid-cols-1 items-center gap-12 lg:grid-cols-2 lg:gap-16">
          {/* Text Column */}
          <div className="max-w-2xl">
            {hero.highlight && (
              <div className="bg-primary-50 mb-6 inline-flex items-center rounded-full px-4 py-1.5 text-sm font-bold uppercase tracking-wider text-primary-700 ring-1 ring-primary-100">
                {hero.highlight}
              </div>
            )}

            <h1 className="mb-6 text-5xl font-extrabold leading-tight tracking-tight text-gray-900 md:text-6xl">
              {hero.title}
            </h1>

            <p className="mb-8 text-xl leading-relaxed text-gray-600">
              {hero.description}
            </p>

            <div className="flex flex-col gap-4 sm:flex-row">
              <Link href={hero.buttonLink || '#'}>
                <Button xl>{hero.button || 'Learn More'}</Button>
              </Link>

              {/* Secondary Button Style */}
              <Link href="#">
                <div className="flex cursor-pointer items-center justify-center rounded-md border-2 border-gray-200 bg-transparent px-8 py-3.5 text-lg font-bold text-gray-700 transition-colors hover:border-gray-300 hover:bg-gray-50">
                  Contact Support
                </div>
              </Link>
            </div>
          </div>

          {/* Image Column */}
          <div className="relative mx-auto w-full lg:max-w-none">
            <div className="relative overflow-hidden rounded-2xl bg-gray-100 shadow-xl ring-1 ring-gray-900/5 transition-transform duration-500 hover:scale-[1.01]">
              <div className="aspect-[4/3] w-full">
                {hero.image ? (
                  <img
                    src={hero.image}
                    alt={hero.title}
                    className="size-full object-cover"
                  />
                ) : (
                  <div className="flex size-full items-center justify-center bg-gray-100 text-gray-400">
                    Image Placeholder
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </Section>
    </Background>
  );
};

export { Hero };
