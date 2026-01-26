import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Banner } from './Banner';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { Sponsors } from './Sponsors';
import { VerticalFeatures } from './VerticalFeatures';

const Base = () => {
  const config = AppConfig as any;
  const title = config?.title || 'Landing Page';
  const description = config?.description || 'Descrição do site.';

  return (
    <div className="bg-white text-gray-900 antialiased selection:bg-black selection:text-white">
      <Meta title={title} description={description} />

      {/* Container principal com max-width controlado para leitura confortável */}
      <main className="w-full">
        <Hero />
        <div className="swiss-divider my-12" /> {/* Linha divisória sutil */}
        <Sponsors />
        <div className="swiss-divider my-12" />
        <VerticalFeatures />
        <Banner />
      </main>

      <Footer />
    </div>
  );
};

export { Base };
