import className from 'classnames';

type IButtonProps = {
  xl?: boolean;
  children: string;
};

const Button = (props: IButtonProps) => {
  const btnClass = className({
    'inline-flex items-center justify-center rounded-full font-bold transition-all duration-300 transform hover:-translate-y-1 hover:shadow-glow focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500':
      true,
    'py-3 px-6 text-sm': !props.xl,
    'py-4 px-8 text-lg md:text-xl': props.xl,
    'bg-primary-600 text-white hover:bg-primary-700 shadow-lg shadow-primary-500/30':
      true,
  });

  return <div className={btnClass}>{props.children}</div>;
};

export { Button };
