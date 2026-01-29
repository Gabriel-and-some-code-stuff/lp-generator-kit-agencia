import { useState } from 'react';

import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const FAQItem = ({ item }: { item: { q: string; a: string } }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="overflow-hidden border-b border-gray-100 bg-white last:border-none">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex w-full items-center justify-between py-5 text-left focus:outline-none"
      >
        <span className="text-base font-bold text-gray-900">{item.q}</span>
        <span
          className={`ml-4 flex size-8 shrink-0 items-center justify-center rounded-full transition-colors duration-200 ${isOpen ? 'bg-primary-100 text-primary-600' : 'bg-gray-50 text-gray-400'}`}
        >
          <svg
            className={`size-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </span>
      </button>
      <div
        className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isOpen ? 'max-h-96 pb-5 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="text-sm leading-relaxed text-gray-600">{item.a}</div>
      </div>
    </div>
  );
};

const FAQ = () => {
  const { faq } = AppConfig as any;
  if (!faq) return null;

  return (
    <Section title={faq.title} yPadding="py-16 md:py-20" className="bg-white">
      {' '}
      {/* Reduzido padding e fundo branco */}
      <div className="mx-auto max-w-3xl rounded-2xl border border-gray-100 p-6 md:p-8">
        {faq.questions.map((item: any, index: number) => (
          <FAQItem key={index} item={item} />
        ))}
      </div>
    </Section>
  );
};

export { FAQ };
