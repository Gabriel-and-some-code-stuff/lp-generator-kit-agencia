import type { ReactNode } from 'react';

type ISectionProps = {
  title?: string;
  description?: string;
  yPadding?: string;
  children: ReactNode;
  className?: string; // Adicionado para flexibilidade
};

const Section = (props: ISectionProps) => (
  <div
    className={`mx-auto max-w-screen-xl px-4 sm:px-6 ${
      props.yPadding ? props.yPadding : 'py-16'
    } ${props.className || ''}`}
  >
    {(props.title || props.description) && (
      <div className="mb-16 max-w-3xl md:mb-24">
        {props.title && (
          <h2 className="mb-6 text-4xl font-bold tracking-tighter text-gray-900 md:text-5xl">
            {props.title}
          </h2>
        )}
        {props.description && (
          <div className="border-l-2 border-gray-200 pl-6 text-xl leading-relaxed text-gray-500">
            {props.description}
          </div>
        )}
      </div>
    )}

    {props.children}
  </div>
);

export { Section };
