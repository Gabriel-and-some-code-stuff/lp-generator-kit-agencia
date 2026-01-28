import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Benefits = () => {
  const { benefits } = AppConfig as any;
  if (!benefits) return null;

  return (
    <Section yPadding="py-20 md:py-28">
      <div className="bg-primary-50 rounded-2xl p-8 md:p-16">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="mb-10 text-3xl font-bold text-gray-900 md:text-4xl">
            {benefits.title}
          </h2>
          <div className="grid gap-6 text-left sm:grid-cols-2">
            {benefits.items.map((item: string, index: number) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="shrink-0">
                  <svg
                    className="size-6 text-primary-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <span className="text-lg font-medium text-gray-800">
                  {item}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Section>
  );
};

export { Benefits };
