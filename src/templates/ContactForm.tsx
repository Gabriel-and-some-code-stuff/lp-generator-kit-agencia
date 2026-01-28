import { Section } from '../layout/Section';

const ContactForm = () => (
  <Section yPadding="py-20 md:py-28" className="bg-gray-900 text-white">
    <div className="grid gap-12 lg:grid-cols-2">
      <div>
        <h2 className="mb-6 text-3xl font-bold text-white">
          Fale com um Especialista
        </h2>
        <p className="mb-8 text-lg text-gray-400">
          Preencha o formulário e nossa equipe entrará em contato em até 1 hora
          comercial.
        </p>

        <div className="space-y-4">
          <div className="flex items-center text-gray-300">
            <span className="font-medium">Atendimento Rápido e Humanizado</span>
          </div>
          <div className="flex items-center text-gray-300">
            <span className="font-medium">Orçamento sem compromisso</span>
          </div>
        </div>
      </div>

      <div className="rounded-xl bg-white p-8 text-gray-900">
        <form className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-bold text-gray-700">
              Nome Completo
            </label>
            <input
              type="text"
              className="w-full rounded-md border border-gray-300 p-3 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
              placeholder="Seu nome"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-bold text-gray-700">
              E-mail Corporativo
            </label>
            <input
              type="email"
              className="w-full rounded-md border border-gray-300 p-3 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
              placeholder="seu@email.com"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-bold text-gray-700">
              Mensagem
            </label>
            <textarea
              className="h-32 w-full rounded-md border border-gray-300 p-3 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
              placeholder="Como podemos ajudar?"
            />
          </div>
          <button
            type="button"
            className="w-full rounded-md bg-primary-600 py-4 text-base font-bold text-white transition-colors hover:bg-primary-700"
          >
            Enviar Mensagem
          </button>
        </form>
      </div>
    </div>
  </Section>
);

export { ContactForm };
