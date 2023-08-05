Object.defineProperty(exports, "__esModule", { value: true });
exports.Assembly = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var Assembly = function (_a) {
    var name = _a.name, version = _a.version, culture = _a.culture, publicKeyToken = _a.publicKeyToken, filePath = _a.filePath;
    return (<AssemblyWrapper>
    <AssemblyInfo>
      <Caption>Assembly:</Caption>
      {name || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{locale_1.t('Version')}:</Caption>
      {version || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{locale_1.t('Culture')}:</Caption>
      {culture || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>PublicKeyToken:</Caption>
      {publicKeyToken || '-'}
    </AssemblyInfo>

    {filePath && (<FilePathInfo>
        <Caption>{locale_1.t('Path')}:</Caption>
        <tooltip_1.default title={filePath}>
          <textCopyInput_1.default rtl>{filePath}</textCopyInput_1.default>
        </tooltip_1.default>
      </FilePathInfo>)}
  </AssemblyWrapper>);
};
exports.Assembly = Assembly;
// TODO(ts): we should be able to delete these after disabling react/prop-types rule in tsx functional components
var AssemblyWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 80%;\n  display: flex;\n  flex-wrap: wrap;\n  color: ", ";\n  text-align: center;\n  position: relative;\n  padding: 0 ", " 0 ", ";\n"], ["\n  font-size: 80%;\n  display: flex;\n  flex-wrap: wrap;\n  color: ", ";\n  text-align: center;\n  position: relative;\n  padding: 0 ", " 0 ", ";\n"])), function (p) { return p.theme.textColor; }, space_1.default(3), space_1.default(3));
var AssemblyInfo = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: 15px;\n  margin-bottom: 5px;\n"], ["\n  margin-right: 15px;\n  margin-bottom: 5px;\n"])));
var Caption = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-right: 5px;\n  font-weight: bold;\n"], ["\n  margin-right: 5px;\n  font-weight: bold;\n"])));
var FilePathInfo = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: 5px;\n  input {\n    width: 300px;\n    height: 20px;\n    padding-top: 0;\n    padding-bottom: 0;\n    line-height: 1.5;\n    @media (max-width: ", ") {\n      width: auto;\n    }\n  }\n  button > span {\n    padding: 2px 5px;\n  }\n  svg {\n    width: 11px;\n    height: 11px;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: 5px;\n  input {\n    width: 300px;\n    height: 20px;\n    padding-top: 0;\n    padding-bottom: 0;\n    line-height: 1.5;\n    @media (max-width: ", ") {\n      width: auto;\n    }\n  }\n  button > span {\n    padding: 2px 5px;\n  }\n  svg {\n    width: 11px;\n    height: 11px;\n  }\n"])), theme_1.default.breakpoints[1]);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=assembly.jsx.map