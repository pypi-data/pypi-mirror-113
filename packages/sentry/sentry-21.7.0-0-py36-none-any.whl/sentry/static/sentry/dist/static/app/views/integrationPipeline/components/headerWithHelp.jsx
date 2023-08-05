Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var logoSentry_1 = tslib_1.__importDefault(require("app/components/logoSentry"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function HeaderWithHelp(_a) {
    var docsUrl = _a.docsUrl;
    return (<Header>
      <StyledLogoSentry />
      <button_1.default external href={docsUrl} size="xsmall">
        {locale_1.t('Need Help?')}
      </button_1.default>
    </Header>);
}
exports.default = HeaderWithHelp;
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: space-between;\n  top: 0;\n  z-index: 100;\n  padding: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: space-between;\n  top: 0;\n  z-index: 100;\n  padding: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n"])), space_1.default(2), function (p) { return p.theme.background; }, function (p) { return p.theme.innerBorder; });
var StyledLogoSentry = styled_1.default(logoSentry_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=headerWithHelp.jsx.map