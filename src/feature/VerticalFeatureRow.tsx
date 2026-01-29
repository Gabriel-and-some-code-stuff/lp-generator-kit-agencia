import { useRouter } from 'next/router';

type IVerticalFeatureRowProps = {
  title: string;
  description: string;
  image: string;
  imageAlt: string;
  reverse?: boolean;
};

const VerticalFeatureRow = (props: IVerticalFeatureRowProps) => {
  const router = useRouter();
  const safeImage = props.image || '';
  const imagePath = safeImage.startsWith('http')
    ? safeImage
    : `${router.basePath}${safeImage}`;

  return (
    <div className="group flex h-full flex-col overflow-hidden rounded-xl border border-gray-200 bg-white transition-all hover:border-primary-100 hover:shadow-lg">
      <div className="relative aspect-[16/10] w-full overflow-hidden bg-gray-100">
        {safeImage ? (
          <img
            src={imagePath}
            alt={props.imageAlt}
            className="size-full object-cover transition-transform duration-700 group-hover:scale-105"
          />
        ) : (
          <div className="flex size-full items-center justify-center bg-gray-50 text-gray-300">
            <span className="text-sm font-medium">Sem imagem</span>
          </div>
        )}
      </div>

      <div className="flex flex-1 flex-col p-6">
        <h3 className="mb-3 text-xl font-bold leading-tight text-gray-900 group-hover:text-primary-700">
          {props.title}
        </h3>
        <p className="flex-1 text-base leading-relaxed text-gray-600">
          {props.description}
        </p>
      </div>
    </div>
  );
};

export { VerticalFeatureRow };
