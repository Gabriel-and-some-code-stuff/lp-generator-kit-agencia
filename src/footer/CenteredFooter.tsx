import type { ReactNode } from 'react';

import { FooterCopyright } from './FooterCopyright';
import { FooterIconList } from './FooterIconList';

type ICenteredFooterProps = {
  logo: ReactNode;
  iconList: ReactNode;
  children: ReactNode;
};

const CenteredFooter = (props: ICenteredFooterProps) => (
  <div className="flex flex-col items-center text-center md:items-start md:text-left">
    <div className="mb-8">{props.logo}</div>

    <nav className="mb-8 w-full">
      <ul className="flex flex-col gap-4 text-sm font-medium uppercase tracking-wider text-gray-600 md:flex-row md:gap-8">
        {props.children}
      </ul>
    </nav>

    <div className="my-8 w-full border-t border-gray-100"></div>

    <div className="flex w-full flex-col items-center justify-between gap-4 md:flex-row">
      <div className="text-xs text-gray-400">
        <FooterCopyright />
      </div>
      <div className="flex">
        <FooterIconList>{props.iconList}</FooterIconList>
      </div>
    </div>
  </div>
);

export { CenteredFooter };
