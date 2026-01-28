import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Problem = () => {
  const { problem } = AppConfig as any;
  if (!problem) return null;

  return (
    <Section yPadding="py-20 md:py-28" className="bg-gray-50">
      <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:items-center">
        <div>
          <h2 className="mb-6 text-3xl font-bold leading-tight text-gray-900 md:text-4xl">
            {problem.title}
          </h2>
          <p className="text-lg leading-relaxed text-gray-600">
            {problem.description}
          </p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          {problem.items.map((item: string, index: number) => (
            <div
              key={index}
              className="shadow-card flex items-start rounded-lg bg-white p-5 transition-transform hover:-translate-y-1"
            >
              <div className="mr-3 mt-1 flex size-6 shrink-0 items-center justify-center rounded-full bg-red-100">
                <svg
                  className="size-4 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </div>
              <span className="font-medium text-gray-800">{item}</span>
            </div>
          ))}
        </div>
      </div>
    </Section>
  );
};

export { Problem };
