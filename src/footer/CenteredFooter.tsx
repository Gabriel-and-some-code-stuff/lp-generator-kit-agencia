import type { ReactNode } from 'react';

import { FooterCopyright } from './FooterCopyright';
import { FooterIconList } from './FooterIconList';

type ICenteredFooterProps = {
  logo: ReactNode;
  iconList: ReactNode;
  children: ReactNode;
};

const CenteredFooter = (props: ICenteredFooterProps) => (
  <div className="flex flex-col items-center gap-12 text-center md:flex-row md:items-start md:justify-between md:text-left">
    <div className="flex max-w-xs flex-col items-center gap-6 md:items-start">
      <div className="transition-opacity hover:opacity-90">{props.logo}</div>
      <div className="text-sm font-medium text-gray-500">
        <FooterCopyright />
      </div>
    </div>

    <div className="flex flex-col items-center gap-8 md:items-end">
      <nav>
        <ul className="flex flex-wrap justify-center gap-x-8 gap-y-4 font-semibold text-gray-700 md:justify-end">
          {props.children}
        </ul>
      </nav>

      <div className="flex items-center gap-4 opacity-80 transition-opacity hover:opacity-100">
        <FooterIconList>{props.iconList}</FooterIconList>
      </div>
    </div>
  </div>
);

export { CenteredFooter };
