import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Trust = () => {
  const { trust } = AppConfig as any;
  if (!trust || !trust.stats) return null;

  return (
    <div className="border-y border-gray-100 bg-white">
      <Section yPadding="py-10 md:py-12">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4 md:gap-12">
          {trust.stats.map((stat: any, index: number) => (
            <div
              key={index}
              className="flex flex-col items-center justify-center text-center"
            >
              <div className="text-3xl font-extrabold tracking-tight text-primary-600 md:text-4xl">
                {stat.value}
              </div>
              <div className="mt-2 text-sm font-semibold uppercase tracking-wider text-gray-500">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
};

export { Trust };
