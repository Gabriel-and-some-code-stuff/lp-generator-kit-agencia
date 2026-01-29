import className from 'classnames';

type IButtonProps = {
  xl?: boolean;
  children: string;
};

const Button = (props: IButtonProps) => {
  const btnClass = className({
    'inline-flex items-center justify-center rounded-lg font-bold transition-all duration-200 transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500':
      true,
    'py-2.5 px-6 text-sm': !props.xl,
    'py-3.5 px-8 text-lg': props.xl,
    'bg-primary-600 text-white hover:bg-primary-700 shadow-md hover:shadow-lg':
      true,
  });

  return <div className={btnClass}>{props.children}</div>;
};

export { Button };
