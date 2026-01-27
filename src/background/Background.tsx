import type { ReactNode } from 'react';

type IBackgroundProps = {
  children: ReactNode;
  color: string;
};

const Background = (props: IBackgroundProps) => (
  <div className={`${props.color} w-full transition-colors duration-200`}>
    {props.children}
  </div>
);

export { Background };
