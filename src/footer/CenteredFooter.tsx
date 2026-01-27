import type { ReactNode } from 'react';

import { FooterCopyright } from './FooterCopyright';
import { FooterIconList } from './FooterIconList';

type ICenteredFooterProps = {
  logo: ReactNode;
  iconList: ReactNode;
  children: ReactNode;
};

const CenteredFooter = (props: ICenteredFooterProps) => (
  <div className="flex flex-col items-center justify-between gap-8 py-8 md:flex-row md:items-start">
    {/* Coluna da Esquerda: Logo e Info */}
    <div className="flex flex-col items-center text-center md:items-start md:text-left">
      <div className="mb-4">{props.logo}</div>
      <p className="mb-6 max-w-xs text-sm text-gray-500">
        Excelência em serviços corporativos e gestão. Comprometidos com a
        qualidade e transparência.
      </p>
      <div className="text-sm text-gray-400">
        <FooterCopyright />
      </div>
    </div>

    {/* Coluna da Direita: Links e Social */}
    <div className="flex flex-col items-center gap-6 md:items-end">
      <nav>
        <ul className="flex flex-wrap justify-center gap-6 text-sm font-medium text-gray-600 md:justify-end">
          {props.children}
        </ul>
      </nav>

      <div className="flex items-center gap-4">
        <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">
          Siga-nos:
        </span>
        <FooterIconList>{props.iconList}</FooterIconList>
      </div>
    </div>
  </div>
);

export { CenteredFooter };
