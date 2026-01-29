import Link from 'next/link';
import type { ReactNode } from 'react';

type INavbarProps = {
  logo: ReactNode;
  children: ReactNode;
};

const NavbarTwoColumns = (props: INavbarProps) => (
  <div className="fixed inset-x-0 top-0 z-50 border-b border-gray-100 bg-white/95 backdrop-blur-md">
    {/* Aumentado o padding para py-6 (24px) para criar a margem de segurança e aumentar a altura da navbar */}
    <div className="mx-auto flex max-w-screen-xl flex-wrap items-center justify-between p-4 sm:px-6 lg:px-8">
      <div className="flex items-center">
        <Link
          href="/"
          className="flex items-center text-gray-900 transition-opacity duration-200 hover:opacity-80"
        >
          {/* Container do logo flexível */}
          <div className="flex items-center">{props.logo}</div>
        </Link>
      </div>

      <nav className="hidden md:block">
        <ul className="flex items-center gap-8 text-sm font-medium text-gray-700">
          {props.children}
        </ul>
      </nav>

      <div className="block md:hidden">
        <button className="rounded-lg bg-gray-50 p-2 text-gray-600 transition-colors hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
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
  </div>
);

export { NavbarTwoColumns };
