import Link from 'next/link';

import { Background } from '../background/Background';
import { CenteredFooter } from '../footer/CenteredFooter';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Footer = () => {
  const config = AppConfig as any;
  const contacts =
    config?.footer?.contacts && Array.isArray(config.footer.contacts)
      ? config.footer.contacts
      : [];

  return (
    <Background color="bg-gray-100">
      <Section>
        <CenteredFooter
          logo={<Logo />}
          iconList={
            <div className="flex gap-4">
              {/* Espaço para ícones sociais futuros */}
            </div>
          }
        >
          <li className="font-medium text-gray-800">
            <Link href="/">Início</Link>
          </li>

          {contacts.length > 0 ? (
            contacts.map((contact: string, index: number) => (
              <li key={index} className="text-gray-600">
                {contact}
              </li>
            ))
          ) : (
            <li className="text-gray-600">Contato via Website</li>
          )}
        </CenteredFooter>
      </Section>
    </Background>
  );
};

export { Footer };
