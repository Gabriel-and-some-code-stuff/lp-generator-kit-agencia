import type { ReactNode } from 'react';

type IHeroOneButtonProps = {
  title: ReactNode;
  description: string;
  button: ReactNode;
};

const HeroOneButton = (props: IHeroOneButtonProps) => (
  <header className="mx-auto flex max-w-5xl flex-col items-center text-center">
    <h1 className="mb-8 whitespace-pre-line text-5xl font-extrabold leading-tight tracking-tight text-gray-900 md:text-6xl lg:leading-[1.1]">
      {props.title}
    </h1>

    <div className="mb-10 max-w-2xl text-xl leading-relaxed text-gray-600 md:text-2xl">
      {props.description}
    </div>

    <div className="mt-2">{props.button}</div>
  </header>
);

export { HeroOneButton };
