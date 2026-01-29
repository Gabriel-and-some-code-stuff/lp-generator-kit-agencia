import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Benefits = () => {
  const { benefits } = AppConfig as any;
  if (!benefits) return null;

  return (
    <Section
      yPadding="py-16 md:py-24" // Reduzido
      className="bg-white"
    >
      <div className="mx-auto mb-12 max-w-4xl text-center">
        <h2 className="text-3xl font-extrabold text-gray-900 md:text-4xl">
          {benefits.title}
        </h2>
      </div>

      <div className="mx-auto grid max-w-5xl gap-6 sm:grid-cols-2 lg:grid-cols-2">
        {benefits.items.map((item: string, index: number) => (
          <div
            key={index}
            className="flex items-center space-x-4 rounded-xl border border-gray-100 bg-white p-6 shadow-sm transition-all hover:border-primary-100 hover:shadow-md"
          >
            <div className="bg-primary-50 flex size-10 shrink-0 items-center justify-center rounded-lg text-primary-600">
              <svg
                className="size-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2.5}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <span className="text-lg font-medium text-gray-800">{item}</span>
          </div>
        ))}
      </div>
    </Section>
  );
};

export { Benefits };
