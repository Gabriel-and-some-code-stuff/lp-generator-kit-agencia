import type { ReactNode } from 'react';

type IFooterIconListProps = {
  children: ReactNode;
};

const FooterIconList = (props: IFooterIconListProps) => (
  <div className="footer-icon-list flex items-center gap-5">
    {props.children}

    <style jsx>
      {`
        .footer-icon-list :global(a) {
          @apply text-gray-400 hover:text-primary-500 transition-colors duration-300;
        }

        .footer-icon-list :global(svg) {
          @apply h-6 w-6 fill-current;
        }
      `}
    </style>
  </div>
);

export { FooterIconList };
