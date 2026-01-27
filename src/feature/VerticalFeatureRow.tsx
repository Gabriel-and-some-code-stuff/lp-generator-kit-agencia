import { useRouter } from 'next/router';

type IVerticalFeatureRowProps = {
  title: string;
  description: string;
  image: string;
  imageAlt: string;
  reverse?: boolean; // Mantido para compatibilidade, mas usado para variação de estilo
};

const VerticalFeatureRow = (props: IVerticalFeatureRowProps) => {
  const router = useRouter();
  const safeImage = props.image || '';
  const imagePath = safeImage.startsWith('http')
    ? safeImage
    : `${router.basePath}${safeImage}`;

  // Design transformado em CARD (Estilo Grid) ao invés de linha
  return (
    <div className="group flex h-full flex-col overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary-100 hover:shadow-xl hover:shadow-primary-900/5">
      {/* Área da Imagem/Ícone */}
      <div className="relative h-48 w-full overflow-hidden bg-gray-50">
        <img
          src={imagePath}
          alt={props.imageAlt}
          className="size-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        {/* Overlay sutil */}
        <div className="absolute inset-0 bg-primary-900/0 transition-colors group-hover:bg-primary-900/5" />
      </div>

      {/* Conteúdo do Card */}
      <div className="flex flex-1 flex-col p-6">
        <h3 className="mb-3 text-xl font-bold text-gray-900 group-hover:text-primary-600">
          {props.title}
        </h3>
        <p className="flex-1 text-sm leading-relaxed text-gray-600">
          {props.description}
        </p>

        <div className="mt-6">
          <span className="inline-flex items-center text-sm font-bold text-primary-600 group-hover:underline">
            Saiba mais
            <svg
              className="ml-2 size-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17 8l4 4m0 0l-4 4m4-4H3"
              />
            </svg>
          </span>
        </div>
      </div>
    </div>
  );
};

export { VerticalFeatureRow };
