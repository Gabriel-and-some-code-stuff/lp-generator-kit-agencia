import className from 'classnames';

type IButtonProps = {
  xl?: boolean;
  children: string;
};

const Button = (props: IButtonProps) => {
  const btnClass = className({
    'inline-block rounded-md text-center font-bold tracking-wide transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg focus:ring-4 focus:ring-primary-200':
      true,
    'py-3 px-6 text-sm': !props.xl,
    'py-4 px-10 text-lg': props.xl,
    'bg-primary-500 text-white hover:bg-primary-600': true, // Enforce primary color
  });

  return <div className={btnClass}>{props.children}</div>;
};

export { Button };
