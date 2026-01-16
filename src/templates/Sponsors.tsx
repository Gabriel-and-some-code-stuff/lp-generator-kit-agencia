import { Section } from '../layout/Section';

const Sponsors = () => (
  <Section
    yPadding="py-6"
    title="Parceiros"
    description="Tecnologia e inovação para o seu negócio."
  >
    <div className="flex flex-col items-center justify-center rounded-md bg-gray-100 p-8 text-center">
      <div className="mb-4 text-xl font-semibold text-gray-700">
        Transformação Digital por
      </div>
      <div className="text-3xl font-bold text-primary-500">Aiello Digital</div>
      <div className="mt-2 text-sm text-gray-500">
        Estratégia e Crescimento para Empresas
      </div>
    </div>
  </Section>
);

export { Sponsors };
