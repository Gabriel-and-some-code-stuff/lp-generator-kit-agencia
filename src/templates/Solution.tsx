import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Solution = () => {
  const { solution } = AppConfig as any;
  if (!solution) return null;

  return (
    <Section
      title={solution.title}
      description={solution.subtitle}
      yPadding="py-20 md:py-28"
    >
      <div className="grid gap-8 md:grid-cols-3">
        {solution.cards.map((card: any, index: number) => (
          <div
            key={index}
            className="shadow-card hover:shadow-float group relative overflow-hidden rounded-xl border border-gray-100 bg-white p-8 transition-all hover:border-primary-100"
          >
            <div className="bg-primary-50 mb-6 inline-flex size-12 items-center justify-center rounded-lg text-primary-600 transition-colors group-hover:bg-primary-600 group-hover:text-white">
              <svg
                className="size-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <h3 className="mb-3 text-xl font-bold text-gray-900">
              {card.title}
            </h3>
            <p className="leading-relaxed text-gray-600">{card.description}</p>
          </div>
        ))}
      </div>
    </Section>
  );
};

export { Solution };
