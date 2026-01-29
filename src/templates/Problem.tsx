import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Problem = () => {
  const { problem } = AppConfig as any;
  if (!problem) return null;

  return (
    <Section yPadding="py-20 md:py-28" className="bg-gray-50">
      <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:items-center">
        <div>
          <div className="mb-4 inline-flex items-center rounded-md bg-red-50 px-3 py-1 text-xs font-bold uppercase tracking-wider text-red-600 ring-1 ring-inset ring-red-600/10">
            O Problema
          </div>
          <h2 className="mb-6 text-3xl font-bold leading-tight text-gray-900 md:text-4xl">
            {problem.title}
          </h2>
          <p className="text-lg leading-relaxed text-gray-600">
            {problem.description}
          </p>
        </div>

        <div className="space-y-4">
          {problem.items.map((item: string, index: number) => (
            <div
              key={index}
              className="flex items-start rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
            >
              <div className="mr-4 mt-1 flex size-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-red-600">
                <svg
                  className="size-3.5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2.5}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </div>
              <span className="text-base font-medium text-gray-700">
                {item}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Section>
  );
};

export { Problem };
