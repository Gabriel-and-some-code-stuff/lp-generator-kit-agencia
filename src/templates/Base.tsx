import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Banner } from './Banner';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { Sponsors } from './Sponsors';
import { VerticalFeatures } from './VerticalFeatures';

const Base = () => {
  const config = AppConfig as any;
  const title = config?.title || 'Qualitas Style Landing';
  const description = config?.description || 'Professional Business Solutions';

  return (
    <div className="flex min-h-screen flex-col bg-white font-sans text-gray-900 antialiased selection:bg-primary-100 selection:text-primary-900">
      <Meta title={title} description={description} />

      {/* Sections stacked with clear vertical rhythm */}
      <Hero />
      <Sponsors />
      <VerticalFeatures />
      <Banner />
      <Footer />
    </div>
  );
};

export { Base };
