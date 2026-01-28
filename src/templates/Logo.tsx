import { AppConfig } from '../utils/AppConfig';

type ILogoProps = {
  xl?: boolean;
};

const Logo = (props: ILogoProps) => {
  const config = AppConfig as any;
  const logoData = config?.logo || {};
  const logoUrl = typeof logoData === 'string' ? logoData : logoData.url;
  const siteName = config?.site_name || 'Brand';

  if (logoUrl) {
    return (
      <img
        src={logoUrl}
        alt={siteName}
        className={`${props.xl ? 'h-10 md:h-12' : 'h-8 md:h-9'} w-auto object-contain`}
      />
    );
  }

  const fontStyle = props.xl
    ? 'font-extrabold text-3xl tracking-tight'
    : 'font-bold text-xl tracking-tight';

  return (
    <div className={`flex items-center gap-2.5 text-gray-900 ${fontStyle}`}>
      <div
        className={`rounded bg-primary-600 ${props.xl ? 'size-8' : 'size-6'}`}
      />
      <span>{siteName}</span>
    </div>
  );
};

export { Logo };
