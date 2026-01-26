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
    <Background color="bg-white border-t border-gray-200">
      <Section yPadding="py-12">
        <CenteredFooter
          logo={<Logo />}
          iconList={
            <div className="flex gap-4 opacity-50 transition-opacity hover:opacity-100">
              {/* Espaço reservado para ícones sociais se necessário */}
            </div>
          }
        >
          {contacts.length > 0 ? (
            contacts.map((contact: string, index: number) => (
              <li
                key={index}
                className="text-sm font-medium text-gray-500 transition-colors hover:text-gray-900"
              >
                {contact}
              </li>
            ))
          ) : (
            <li className="text-sm font-medium text-gray-500">
              Entre em contato conosco
            </li>
          )}
        </CenteredFooter>
      </Section>
    </Background>
  );
};

export { Footer };
