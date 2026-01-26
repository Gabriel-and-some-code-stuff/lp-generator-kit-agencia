import className from 'classnames';
import { useRouter } from 'next/router';

type IVerticalFeatureRowProps = {
  title: string;
  description: string;
  image: string;
  imageAlt: string;
  reverse?: boolean;
};

const VerticalFeatureRow = (props: IVerticalFeatureRowProps) => {
  const verticalFeatureClass = className(
    'mt-20',
    'flex',
    'flex-wrap',
    'items-center',
    {
      'flex-row-reverse': props.reverse,
    },
  );

  const router = useRouter();

  // Tratamento robusto de imagem
  const safeImage = props.image || '';
  const isExternalImage =
    safeImage.startsWith('http') || safeImage.startsWith('https');

  // Lógica clara de seleção de imagem (evita erros de sintaxe e lógica)
  let imagePath;
  if (safeImage === '') {
    imagePath = '/assets/images/feature.svg'; // Fallback local
  } else if (isExternalImage) {
    imagePath = safeImage;
  } else {
    imagePath = `${router.basePath}${safeImage}`;
  }

  return (
    <div className={verticalFeatureClass}>
      <div className="w-full text-center sm:w-1/2 sm:px-6">
        <h3 className="text-3xl font-semibold text-gray-900">{props.title}</h3>
        <div className="mt-6 text-xl leading-9">{props.description}</div>
      </div>

      <div className="w-full p-6 sm:w-1/2">
        <img
          src={imagePath}
          alt={props.imageAlt}
          className="rounded-lg shadow-md"
        />
      </div>
    </div>
  );
};

export { VerticalFeatureRow };
