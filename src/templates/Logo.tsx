import { AppConfig } from '../utils/AppConfig';

type ILogoProps = {
  xl?: boolean;
};

const Logo = (props: ILogoProps) => {
  const config = AppConfig as any;
  const siteName = config?.site_name || 'Landing Page';

  const fontStyle = props.xl
    ? 'font-bold text-3xl tracking-tighter'
    : 'font-bold text-xl tracking-tight';

  return (
    <span className={`inline-flex items-center text-gray-900 ${fontStyle}`}>
      {/* Ícone geométrico minimalista (quadrado) */}
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
