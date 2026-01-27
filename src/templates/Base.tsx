import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Banner } from './Banner';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { Sponsors } from './Sponsors';
import { VerticalFeatures } from './VerticalFeatures';

const Base = () => {
  const config = AppConfig as any;
  const title = config?.title || 'Qualitas Payroll Services';
  const description = config?.description || 'Professional Payroll Services.';

  return (
    <div className="flex min-h-screen flex-col bg-white font-sans text-gray-900 antialiased">
      <Meta title={title} description={description} />

      <Hero />

      {/* Barra de confiança logo após o Hero para autoridade imediata */}
      <Sponsors />

      {/* Seção principal de serviços em Grid */}
      <VerticalFeatures />

      {/* CTA Final */}
      <Banner />

      <Footer />
    </div>
  );
};

export { Base };
