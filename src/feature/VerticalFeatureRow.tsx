import className from 'classnames';
import { useRouter } from 'next/router';

type IVerticalFeatureRowProps = {
  title: string;
  description: string;
  image: string;
  imageAlt: string;
  reverse?: boolean;
  index?: number; // Adicionado para numeração
};

const VerticalFeatureRow = (props: IVerticalFeatureRowProps) => {
  const router = useRouter();
  const safeImage = props.image || '';
  const imagePath = safeImage.startsWith('http')
    ? safeImage
    : `${router.basePath}${safeImage || '/assets/images/feature.svg'}`;

  // Formata número (01, 02...)
  const number = props.index ? props.index.toString().padStart(2, '0') : '00';

  return (
    <div
      className={className(
        'grid grid-cols-1 md:grid-cols-2 gap-12 items-center border-t border-gray-100 pt-12',
        {
          '': props.reverse,
        },
      )}
    >
      <div
        className={className('order-2 md:order-1', {
          'md:order-2': props.reverse,
        })}
      >
        <span className="mb-4 block font-mono text-xs text-gray-400">
          ({number})
        </span>
        <h3 className="mb-6 text-3xl font-bold tracking-tight text-gray-900">
          {props.title}
        </h3>
        <p className="max-w-md text-lg leading-relaxed text-gray-600">
          {props.description}
        </p>
      </div>

      <div
        className={className(
          'order-1 md:order-2 relative aspect-video bg-gray-50',
          { 'md:order-1': props.reverse },
        )}
      >
        <img
          src={imagePath}
          alt={props.imageAlt}
          className="size-full object-cover grayscale transition-all duration-500 hover:grayscale-0"
        />
      </div>
    </div>
  );
};

export { VerticalFeatureRow };
