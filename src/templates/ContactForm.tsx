import { Section } from '../layout/Section';

const ContactForm = () => (
  <Section
    yPadding="py-12 md:py-20"
    className="bg-primary-50/30 border-t border-primary-100/50"
  >
    <div className="mx-auto max-w-4xl rounded-2xl border border-gray-100 bg-white p-6 shadow-xl shadow-gray-200/50 md:p-10">
      <div className="mb-8 text-center">
        <h2 className="mb-3 text-2xl font-extrabold text-gray-900 md:text-3xl">
          Vamos tirar seu projeto do papel?
        </h2>
        <p className="mx-auto max-w-2xl text-base text-gray-500">
          Preencha os dados abaixo. Nossa equipe entrará em contato para
          entender sua necessidade.
        </p>
      </div>

      <form className="grid gap-4 md:grid-cols-2">
        <div className="col-span-2 md:col-span-1">
          <label className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-gray-500">
            Nome Completo
          </label>
          <input
            type="text"
            className="w-full rounded-lg border border-gray-300 bg-gray-50 p-3 text-gray-900 transition-colors focus:border-primary-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="Ex: Maria Silva"
          />
        </div>

        <div className="col-span-2 md:col-span-1">
          <label className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-gray-500">
            WhatsApp
          </label>
          <input
            type="tel"
            className="w-full rounded-lg border border-gray-300 bg-gray-50 p-3 text-gray-900 transition-colors focus:border-primary-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="(00) 00000-0000"
          />
        </div>

        <div className="col-span-2">
          <label className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-gray-500">
            E-mail Profissional
          </label>
          <input
            type="email"
            className="w-full rounded-lg border border-gray-300 bg-gray-50 p-3 text-gray-900 transition-colors focus:border-primary-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="exemplo@empresa.com"
          />
        </div>

        <div className="col-span-2">
          <label className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-gray-500">
            Mensagem
          </label>
          <textarea
            rows={3}
            className="w-full rounded-lg border border-gray-300 bg-gray-50 p-3 text-gray-900 transition-colors focus:border-primary-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="Descreva brevemente sua necessidade..."
          />
        </div>

        <div className="col-span-2 mt-2">
          <button
            type="button"
            className="w-full rounded-lg bg-primary-600 py-3.5 text-base font-bold text-white shadow-lg shadow-primary-600/20 transition-all hover:-translate-y-1 hover:bg-primary-700 hover:shadow-xl"
          >
            Solicitar Orçamento Gratuito
          </button>
          <p className="mt-3 text-center text-xs text-gray-400">
            Seus dados estão protegidos.
          </p>
        </div>
      </form>
    </div>
  </Section>
);

export { ContactForm };
