import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Problem = () => {
  const { problem } = AppConfig as any;
  if (!problem) return null;

  return (
    <Section yPadding="py-12 md:py-20" className="bg-gray-50/50">
      <div className="grid grid-cols-1 gap-10 lg:grid-cols-2 lg:items-center">
        <div>
          <div className="mb-3 inline-block rounded-full bg-red-100 px-3 py-1 text-xs font-bold uppercase tracking-wide text-red-600">
            O Desafio
          </div>
          <h2 className="mb-4 text-2xl font-extrabold leading-tight text-gray-900 md:text-3xl">
            {problem.title}
          </h2>
          <p className="text-base leading-relaxed text-gray-600">
            {problem.description}
          </p>
        </div>

        <div className="grid gap-4">
          {problem.items.map((item: string, index: number) => (
            <div
              key={index}
              className="flex items-start rounded-xl border border-gray-100 bg-white p-4 shadow-sm transition-all hover:scale-[1.01] hover:shadow-md"
            >
              <div className="mr-3 mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-red-600">
                <svg
                  className="size-3.5"
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
              <span className="text-base font-medium text-gray-800">
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
