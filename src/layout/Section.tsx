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
    className={`mx-auto max-w-screen-xl px-6 sm:px-8 ${
      props.yPadding ? props.yPadding : 'py-20 md:py-28'
    } ${props.className || ''}`}
  >
    {(props.title || props.description) && (
      <div className="mb-16 max-w-3xl md:mb-20">
        {props.title && (
          <div className="mb-6">
            <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl md:text-5xl">
              {props.title}
            </h2>
            <div className="mt-4 h-1.5 w-24 rounded-full bg-primary-500" />
          </div>
        )}
        {props.description && (
          <div className="text-xl leading-relaxed text-gray-500">
            {props.description}
          </div>
        )}
      </div>
    )}

    {props.children}
  </div>
);

export { Section };
