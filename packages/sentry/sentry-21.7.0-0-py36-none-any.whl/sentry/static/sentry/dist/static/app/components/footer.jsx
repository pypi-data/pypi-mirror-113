Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var hook_1 = tslib_1.__importDefault(require("app/components/hook"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
function Footer(_a) {
    var className = _a.className;
    var config = configStore_1.default.getConfig();
    return (<footer className={className}>
      <LeftLinks>
        {config.isOnPremise && (<react_1.Fragment>
            {'Sentry '}
            {getDynamicText_1.default({
                fixed: 'Acceptance Test',
                value: config.version.current,
            })}
            <Build>
              {getDynamicText_1.default({
                fixed: 'test',
                value: config.version.build.substring(0, 7),
            })}
            </Build>
          </react_1.Fragment>)}
        {config.privacyUrl && (<FooterLink href={config.privacyUrl}>{locale_1.t('Privacy Policy')}</FooterLink>)}
        {config.termsUrl && (<FooterLink href={config.termsUrl}>{locale_1.t('Terms of Use')}</FooterLink>)}
      </LeftLinks>
      <LogoLink />
      <RightLinks>
        <FooterLink href="/api/">{locale_1.t('API')}</FooterLink>
        <FooterLink href="/docs/">{locale_1.t('Docs')}</FooterLink>
        <FooterLink href="https://github.com/getsentry/sentry">
          {locale_1.t('Contribute')}
        </FooterLink>
        {config.isOnPremise && !config.demoMode && (<FooterLink href="/out/">{locale_1.t('Migrate to SaaS')}</FooterLink>)}
      </RightLinks>
      <hook_1.default name="footer"/>
    </footer>);
}
var LeftLinks = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-start;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-start;\n  gap: ", ";\n"])), space_1.default(2));
var RightLinks = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-end;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-end;\n  gap: ", ";\n"])), space_1.default(2));
var FooterLink = styled_1.default(externalLink_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"], ["\n  color: ", ";\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.blue300; });
var LogoLink = styled_1.default(function (props) { return (<externalLink_1.default href="https://sentry.io/welcome/" tabIndex={-1} {...props}>
    <icons_1.IconSentry size="xl"/>
  </externalLink_1.default>); })(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"], ["\n  color: ", ";\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"])), function (p) { return p.theme.subText; });
var Build = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, function (p) { return p.theme.subText; }, space_1.default(1));
var StyledFooter = styled_1.default(Footer)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n  margin-top: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n  margin-top: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.border; }, space_1.default(4), function (p) { return p.theme.breakpoints[0]; });
exports.default = StyledFooter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=footer.jsx.map