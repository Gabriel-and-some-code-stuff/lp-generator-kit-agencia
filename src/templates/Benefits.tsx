import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Benefits = () => {
  const { benefits } = AppConfig as any;
  if (!benefits) return null;

  return (
    <Section yPadding="py-12 md:py-16" className="bg-white">
      <div className="bg-primary-50 relative overflow-hidden rounded-3xl px-6 py-10 md:px-12 md:py-16">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="mb-8 text-2xl font-extrabold text-gray-900 md:text-3xl">
            {benefits.title}
          </h2>
          <div className="grid gap-x-6 gap-y-4 text-left sm:grid-cols-2">
            {benefits.items.map((item: string, index: number) => (
              <div
                key={index}
                className="flex items-center space-x-3 rounded-xl bg-white/60 p-3 shadow-sm backdrop-blur-sm"
              >
                <div className="flex size-6 shrink-0 items-center justify-center rounded-full bg-primary-100 text-primary-600">
                  <svg
                    className="size-4"
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
                <span className="text-base font-semibold text-gray-800">
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
