import Link from 'next/link';
import type { ReactNode } from 'react';

type INavbarProps = {
  logo: ReactNode;
  children: ReactNode;
};

const NavbarTwoColumns = (props: INavbarProps) => (
  <div className="flex w-full flex-wrap items-center justify-between">
    <div>
      <Link href="/">{props.logo}</Link>
    </div>

    <nav>
      <ul className="flex items-center gap-8 font-medium text-gray-800">
        {props.children}
      </ul>
    </nav>
  </div>
);

export { NavbarTwoColumns };
