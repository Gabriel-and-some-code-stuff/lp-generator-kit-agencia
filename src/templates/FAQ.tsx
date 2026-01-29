import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const FAQ = () => {
  const { faq } = AppConfig as any;
  if (!faq) return null;

  return (
    <Section title={faq.title} yPadding="py-12 md:py-20" className="bg-gray-50">
      <div className="mx-auto max-w-3xl space-y-3">
        {faq.questions.map((item: any, index: number) => (
          <div
            key={index}
            className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-all hover:border-primary-200 hover:shadow-md"
          >
            <h3 className="mb-2 text-base font-bold text-gray-900">{item.q}</h3>
            <p className="text-sm leading-relaxed text-gray-600">{item.a}</p>
          </div>
        ))}
      </div>
    </Section>
  );
};

export { FAQ };
