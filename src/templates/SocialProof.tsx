import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';

const SocialProof = () => {
  const { socialProof } = AppConfig as any;
  if (!socialProof) return null;

  // Lógica para suportar tanto galeria detalhada (objetos) quanto logos simples (strings)
  const hasGallery = socialProof.gallery && socialProof.gallery.length > 0;
  const hasLogos = socialProof.logos && socialProof.logos.length > 0;

  if (
    !hasGallery &&
    !hasLogos &&
    (!socialProof.testimonials || socialProof.testimonials.length === 0)
  ) {
    return null;
  }

  return (
    <Section
      title={socialProof.title}
      yPadding="py-16 md:py-24"
      className="bg-gray-50/50"
    >
      {/* Testimonials Section */}
      <div className="mb-20 grid gap-8 md:grid-cols-3">
        {socialProof.testimonials.map((testim: any, index: number) => (
          <div
            key={index}
            className="flex h-full flex-col justify-between rounded-xl border border-gray-100 bg-white p-8 shadow-sm"
          >
            <div>
              <div className="mb-5 flex text-yellow-400">
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
              <p className="mb-6 text-base italic leading-relaxed text-gray-700">
                &quot;{testim.text}&quot;
              </p>
            </div>
            <div className="flex items-center gap-4 border-t border-gray-100 pt-4">
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

      {/* Gallery / Logos Section */}
      {(hasGallery || hasLogos) && (
        <div className="mt-12 text-center">
          <p className="mb-10 text-sm font-bold uppercase tracking-widest text-gray-400">
            Empresas e Serviços em Destaque
          </p>

          {/* MUDANÇA: Grid Adaptável para Galeria com Legendas */}
          <div className="flex flex-wrap items-stretch justify-center gap-8">
            {hasGallery
              ? socialProof.gallery.map((item: any, index: number) => (
                  <div
                    key={index}
                    className="group relative flex w-full flex-col overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm transition-all hover:-translate-y-1 hover:shadow-md sm:w-64"
                  >
                    <div className="h-48 w-full overflow-hidden bg-gray-100">
                      <img
                        src={item.src}
                        alt={item.alt}
                        className="size-full object-cover transition-transform duration-700 group-hover:scale-105"
                      />
                    </div>
                    <div className="flex flex-1 items-center justify-center border-t border-gray-100 p-4">
                      <p className="text-center text-sm font-bold text-gray-700">
                        {item.alt}
                      </p>
                    </div>
                  </div>
                ))
              : socialProof.logos.map((logo: string, index: number) => (
                  // Fallback para lista de strings (logos simples)
                  <div
                    key={index}
                    className="flex h-24 w-32 items-center justify-center rounded-lg border border-gray-100 bg-white p-4 shadow-sm transition-transform hover:scale-105"
                  >
                    <img
                      src={logo}
                      alt={`Parceiro ${index + 1}`}
                      className="size-full object-contain opacity-70 transition-opacity hover:opacity-100"
                    />
                  </div>
                ))}
          </div>
        </div>
      )}
    </Section>
  );
};

export { SocialProof };
