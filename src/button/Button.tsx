import className from 'classnames';

type IButtonProps = {
  xl?: boolean;
  children: string;
};

const Button = (props: IButtonProps) => {
  const btnClass = className({
    'inline-block text-center transition-all duration-200 border border-transparent cursor-pointer':
      true,
    'text-base py-3 px-6 font-bold uppercase tracking-widest': !props.xl,
    'text-lg py-4 px-10 font-bold uppercase tracking-widest': props.xl,
    'bg-gray-900 text-white hover:bg-white hover:text-gray-900 hover:border-gray-900':
      true, // Efeito Invertido
  });

  return <div className={btnClass}>{props.children}</div>;
};

export { Button };
