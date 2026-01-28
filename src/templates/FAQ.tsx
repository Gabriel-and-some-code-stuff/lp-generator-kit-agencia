import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const FAQ = () => {
  const { faq } = AppConfig as any;
  if (!faq) return null;

  return (
    <Section title={faq.title} yPadding="py-20 md:py-28">
      <div className="mx-auto max-w-3xl space-y-6">
        {faq.questions.map((item: any, index: number) => (
          <div
            key={index}
            className="rounded-lg border border-gray-100 bg-white p-6 shadow-sm"
          >
            <h3 className="mb-2 text-lg font-bold text-gray-900">{item.q}</h3>
            <p className="text-gray-600">{item.a}</p>
          </div>
        ))}
      </div>
    </Section>
  );
};

export { FAQ };
