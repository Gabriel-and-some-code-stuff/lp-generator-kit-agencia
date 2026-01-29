import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const SocialProof = () => {
  const { socialProof } = AppConfig as any;
  if (!socialProof) return null;

  return (
    <Section
      title={socialProof.title}
      yPadding="py-12 md:py-20"
      className="bg-white"
    >
      <div className="mb-12 grid gap-6 md:grid-cols-3">
        {socialProof.testimonials.map((testim: any, index: number) => (
          <div
            key={index}
            className="flex h-full flex-col justify-between rounded-2xl bg-gray-50 p-6 shadow-sm transition-shadow hover:shadow-md"
          >
            <div>
              <div className="mb-4 flex text-yellow-400">
                {[...Array(5)].map((_, i) => (
                  <svg
                    key={i}
                    className="size-4 fill-current"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="mb-4 text-base font-medium leading-relaxed text-gray-700">
                &quot;{testim.text}&quot;
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="size-8 rounded-full bg-gray-300" />
              <div>
                <div className="text-sm font-bold text-gray-900">
                  {testim.name}
                </div>
                <div className="text-xs font-medium text-gray-500">
                  {testim.role}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {socialProof.logos && socialProof.logos.length > 0 && (
        <div className="mt-10 border-t border-gray-100 pt-10">
          <p className="mb-6 text-center text-xs font-bold uppercase tracking-widest text-gray-400">
            Empresas que confiam
          </p>
          <div className="flex flex-wrap justify-center gap-8 opacity-50 grayscale transition-all duration-500 hover:opacity-100 hover:grayscale-0">
            {socialProof.logos.map((logo: string, index: number) => (
              <img
                key={index}
                src={logo}
                alt="Parceiro"
                className="h-6 w-auto object-contain md:h-8"
              />
            ))}
          </div>
        </div>
      )}
    </Section>
  );
};

export { SocialProof };
