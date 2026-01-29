import type { ReactNode } from 'react';

type ISectionProps = {
  title?: string;
  description?: string;
  yPadding?: string;
  children: ReactNode;
  className?: string;
};

const Section = (props: ISectionProps) => (
  <div
    className={`mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8 ${
      props.yPadding ? props.yPadding : 'py-12 md:py-16'
    } ${props.className || ''}`}
  >
    {(props.title || props.description) && (
      <div className="mb-16 text-center md:mb-24">
        {props.title && (
          <h2 className="mb-6 text-3xl font-extrabold leading-tight text-gray-900 md:text-5xl">
            {props.title}
          </h2>
        )}
        {props.description && (
          <div className="mx-auto max-w-3xl text-xl leading-relaxed text-gray-500 md:text-2xl">
            {props.description}
          </div>
        )}
      </div>
    )}

    {props.children}
  </div>
);

export { Section };
