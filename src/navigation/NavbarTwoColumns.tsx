import Link from 'next/link';
import type { ReactNode } from 'react';

type INavbarProps = {
  logo: ReactNode;
  children: ReactNode;
};

const NavbarTwoColumns = (props: INavbarProps) => (
  <div className="flex w-full flex-wrap items-center justify-between">
    <div className="flex items-center">
      <Link href="/">{props.logo}</Link>
    </div>

    <nav className="hidden md:block">
      <ul className="flex items-center gap-8 font-medium text-gray-700">
        {props.children}
      </ul>
    </nav>

    {/* Menu Mobile Simplificado (placeholder) */}
    <div className="block md:hidden">
      <button className="text-gray-600 focus:outline-none">
        <svg
          className="size-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
    </div>
  </div>
);

export { NavbarTwoColumns };
