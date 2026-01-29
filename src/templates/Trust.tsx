import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const Trust = () => {
  const { trust } = AppConfig as any;
  if (!trust || !trust.stats) return null;

  return (
    <div className="border-b border-gray-100 bg-white">
      <Section yPadding="py-8 md:py-10">
        <div className="grid grid-cols-2 gap-6 md:grid-cols-4 md:gap-10">
          {trust.stats.map((stat: any, index: number) => (
            <div
              key={index}
              className="flex flex-col items-center justify-center"
            >
              <div className="text-3xl font-black tracking-tight text-primary-600 md:text-4xl">
                {stat.value}
              </div>
              <div className="mt-1 text-center text-xs font-bold uppercase tracking-wider text-gray-400">
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
