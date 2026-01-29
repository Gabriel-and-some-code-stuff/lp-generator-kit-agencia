import { AppConfig } from '../utils/AppConfig';

const FooterCopyright = () => (
  <div className="footer-copyright">
    &copy; {new Date().getFullYear()}{' '}
    <span className="font-bold text-gray-900">
      {(AppConfig as any).site_name}
    </span>
    .
    <br className="sm:hidden" /> Todos os direitos reservados.
    <style jsx>
      {`
        .footer-copyright :global(a) {
          @apply text-primary-600 hover:text-primary-700 transition-colors duration-200 font-medium;
        }
      `}
    </style>
  </div>
);

export { FooterCopyright };
