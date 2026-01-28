import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Benefits } from './Benefits';
import { ContactForm } from './ContactForm';
import { FAQ } from './FAQ';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { HowItWorks } from './HowitWorks';
import { Problem } from './Problem';
import { SocialProof } from './SocialProof';
import { SoftCTA } from './SoftCTA';
import { Solution } from './Solution';
import { Trust } from './Trust';

const Base = () => {
  const config = AppConfig as any;

  return (
    <div className="flex min-h-screen flex-col bg-white font-sans text-gray-900 antialiased">
      <Meta title={config.title} description={config.description} />

      <Hero />
      <Trust />
      <Problem />
      <Solution />
      <HowItWorks />
      <Benefits />
      <SocialProof />
      <FAQ />
      <SoftCTA />
      <ContactForm />
      <Footer />
    </div>
  );
};

export { Base };
