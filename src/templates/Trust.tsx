import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Trust = () => {
  const { trust } = AppConfig as any;
  if (!trust || !trust.stats) return null;

  return (
    <Section yPadding="py-12" className="border-b border-gray-100 bg-white">
      <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
        {trust.stats.map((stat: any, index: number) => (
          <div key={index} className="text-center">
            <div className="text-4xl font-extrabold text-primary-600">
              {stat.value}
            </div>
            <div className="mt-1 text-sm font-medium uppercase tracking-wider text-gray-500">
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
};

export { Trust };
