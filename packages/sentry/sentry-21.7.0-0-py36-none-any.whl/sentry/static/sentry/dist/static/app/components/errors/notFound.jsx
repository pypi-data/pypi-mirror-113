Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var NotFound = function () { return (<NotFoundAlert type="error" icon={<icons_1.IconInfo size="lg"/>}>
    <Heading>{locale_1.t('Page Not Found')}</Heading>
    <p>{locale_1.t('The page you are looking for was not found.')}</p>
    <p>{locale_1.t('You may wish to try the following:')}</p>
    <ul>
      <li>
        {locale_1.t("If you entered the address manually, double check the path. Did you\n           forget a trailing slash?")}
      </li>
      <li>
        {locale_1.t("If you followed a link here, try hitting back and reloading the\n           page. It's possible the resource was moved out from under you.")}
      </li>
      <li>
        {locale_1.tct('If all else fails, [link:contact us] with more details', {
        link: (<externalLink_1.default href="https://github.com/getsentry/sentry/issues/new/choose"/>),
    })}
      </li>
    </ul>
    <p>
      {locale_1.tct('Not sure what to do? [link:Return to the dashboard]', {
        link: <link_1.default to="/"/>,
    })}
    </p>
  </NotFoundAlert>); };
var NotFoundAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space_1.default(3));
var Heading = styled_1.default('h1')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " 0;\n"], ["\n  font-size: ", ";\n  margin: ", " 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space_1.default(1));
exports.default = NotFound;
var templateObject_1, templateObject_2;
//# sourceMappingURL=notFound.jsx.map