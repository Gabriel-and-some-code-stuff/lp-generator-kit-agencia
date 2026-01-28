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
    <div className="group flex h-full flex-col overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm transition-shadow duration-300 hover:shadow-md">
      <div className="relative aspect-[16/9] w-full overflow-hidden bg-gray-50">
        {safeImage ? (
          <img
            src={imagePath}
            alt={props.imageAlt}
            className="size-full object-cover transition-transform duration-700 group-hover:scale-105"
          />
        ) : (
          <div className="flex size-full items-center justify-center bg-gray-100 text-gray-400">
            <span className="text-sm font-medium">Image not available</span>
          </div>
        )}
      </div>

      <div className="flex flex-1 flex-col p-8">
        <h3 className="mb-4 text-xl font-bold leading-tight text-gray-900 group-hover:text-primary-600">
          {props.title}
        </h3>
        <div className="mb-6 h-1 w-12 rounded-full bg-primary-500/20" />
        <p className="flex-1 text-base leading-relaxed text-gray-600">
          {props.description}
        </p>
      </div>
    </div>
  );
};

export { VerticalFeatureRow };
