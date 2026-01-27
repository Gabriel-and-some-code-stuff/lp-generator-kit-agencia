import { Background } from '../background/Background';
import { CenteredFooter } from '../footer/CenteredFooter';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Footer = () => {
  const config = AppConfig as any;
  const contacts = config?.footer?.contacts || [];
  const links = config?.footer?.links || []; // Support for link list if present in config

  // Qualitas Style: Footer is substantial, high contrast or visually grounded.
  return (
    <Background color="bg-gray-50 border-t border-gray-200">
      <Section yPadding="py-16 md:py-24">
        <CenteredFooter logo={<Logo />} iconList={<></>}>
          {/* Render links if available, otherwise contacts */}
          {(links.length > 0 ? links : contacts).map(
            (item: any, index: number) => {
              const label = typeof item === 'string' ? item : item.label;
              const link = typeof item === 'string' ? '#' : item.link;

              return (
                <li key={index}>
                  <a
                    href={link}
                    className="text-gray-600 transition-colors hover:text-primary-600"
                  >
                    {label}
                  </a>
                </li>
              );
            },
          )}
        </CenteredFooter>
      </Section>
    </Background>
  );
};

export { Footer };
