import { AppConfig } from '../utils/AppConfig';

type ILogoProps = {
  xl?: boolean;
};

const Logo = (props: ILogoProps) => {
  const config = AppConfig as any;
  const logoUrl = config?.logo?.url || '';
  const logoAlt = config?.logo?.alt || config?.site_name || 'Logo';
  const siteName = config?.site_name || 'Landing Page';

  if (logoUrl) {
    return (
      <img
        src={logoUrl}
        alt={logoAlt}
        // Aumentando ainda mais o tamanho para o modo XL (Hero) e ajustando a responsividade
        className={`object-contain ${props.xl ? 'h-24 max-w-[280px] md:h-32' : 'h-16 max-w-[200px] md:h-20'} w-auto`}
      />
    );
  }

  const fontStyle = props.xl
    ? 'font-bold text-3xl tracking-tighter'
    : 'font-bold text-xl tracking-tight';

  return (
    <span className={`inline-flex items-center text-gray-900 ${fontStyle}`}>
      <svg
        className="mr-3 size-5 text-primary-600"
        viewBox="0 0 24 24"
        fill="currentColor"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="24" height="24" />
      </svg>
      {siteName}
    </span>
  );
};

export { Logo };
