import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Banner } from './Banner';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { Sponsors } from './Sponsors';
import { VerticalFeatures } from './VerticalFeatures';

const Base = () => {
  const config = AppConfig as any;
  const title = config?.title || 'Landing Page Gerada';
  const description = config?.description || 'Descrição do site.';

  return (
    <div className="text-gray-600 antialiased">
      <Meta title={title} description={description} />
      <Hero />
      <Sponsors />
      <VerticalFeatures />
      <Banner />
      <Footer />
    </div>
  );
};

export { Base };
