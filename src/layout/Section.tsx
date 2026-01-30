import type { ReactNode } from 'react';

type ISectionProps = {
  title?: string;
  description?: string;
  yPadding?: string;
  children: ReactNode;
  className?: string;
  id?: string; // ADICIONADO: Propriedade ID opcional
};

const Section = (props: ISectionProps) => (
  <div
    id={props.id} // ADICIONADO: Aplica o ID na div principal
    className={`mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8 ${
      props.yPadding ? props.yPadding : 'py-16 md:py-24'
    } ${props.className || ''}`}
  >
    {(props.title || props.description) && (
      <div className="mx-auto mb-10 max-w-3xl text-center md:mb-12">
        {props.title && (
          <h2 className="mb-4 text-3xl font-extrabold tracking-tight text-gray-900 md:text-4xl">
            {props.title}
          </h2>
        )}
        {props.description && (
          <div className="text-lg leading-relaxed text-gray-600">
            {props.description}
          </div>
        )}
      </div>
    )}

    {props.children}
  </div>
);

export { Section };
