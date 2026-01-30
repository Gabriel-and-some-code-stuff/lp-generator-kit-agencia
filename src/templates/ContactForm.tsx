import { Section } from '../layout/Section';

const ContactForm = () => (
  <Section
    id="contact" // CORREÇÃO: Adicionado ID para ancoragem
    yPadding="py-16 md:py-20"
    className="border-t border-gray-100 bg-white"
  >
    <div className="mx-auto max-w-4xl overflow-hidden rounded-xl border border-gray-200 bg-white p-8 md:p-12">
      <div className="mb-8 text-center">
        <h2 className="mb-3 text-3xl font-extrabold text-gray-900">
          Vamos conversar?
        </h2>
        <p className="mx-auto max-w-2xl text-lg text-gray-500">
          Preencha os dados abaixo para solicitar um orçamento ou tirar dúvidas.
        </p>
      </div>

      <form className="mx-auto grid gap-6 md:grid-cols-2">
        <div className="col-span-2 md:col-span-1">
          <label className="mb-2 block text-sm font-semibold text-gray-700">
            Nome Completo
          </label>
          <input
            type="text"
            className="w-full rounded-lg border border-gray-300 bg-white p-3 text-gray-900 shadow-sm transition-all focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="Seu nome"
          />
        </div>

        <div className="col-span-2 md:col-span-1">
          <label className="mb-2 block text-sm font-semibold text-gray-700">
            WhatsApp / Telefone
          </label>
          <input
            type="tel"
            className="w-full rounded-lg border border-gray-300 bg-white p-3 text-gray-900 shadow-sm transition-all focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="(00) 00000-0000"
          />
        </div>

        <div className="col-span-2">
          <label className="mb-2 block text-sm font-semibold text-gray-700">
            E-mail Profissional
          </label>
          <input
            type="email"
            className="w-full rounded-lg border border-gray-300 bg-white p-3 text-gray-900 shadow-sm transition-all focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="seu@email.com"
          />
        </div>

        <div className="col-span-2">
          <label className="mb-2 block text-sm font-semibold text-gray-700">
            Como podemos ajudar?
          </label>
          <textarea
            rows={4}
            className="w-full rounded-lg border border-gray-300 bg-white p-3 text-gray-900 shadow-sm transition-all focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            placeholder="Descreva sua necessidade..."
          />
        </div>

        <div className="col-span-2 mt-2">
          <button
            type="button"
            className="w-full rounded-lg bg-primary-600 py-3.5 text-base font-bold text-white shadow-sm transition-all hover:bg-primary-700 hover:shadow-md"
          >
            Enviar Mensagem
          </button>
          <p className="mt-4 text-center text-xs text-gray-400">
            Respeitamos sua privacidade. Seus dados estão seguros.
          </p>
        </div>
      </form>
    </div>
  </Section>
);

export { ContactForm };
