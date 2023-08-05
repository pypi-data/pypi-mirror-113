Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
function SimilarSpectrum(_a) {
    var className = _a.className;
    return (<div className={className}>
      <span>{locale_1.t('Similar')}</span>
      <SpectrumItem colorIndex={4}/>
      <SpectrumItem colorIndex={3}/>
      <SpectrumItem colorIndex={2}/>
      <SpectrumItem colorIndex={1}/>
      <SpectrumItem colorIndex={0}/>
      <span>{locale_1.t('Not Similar')}</span>
    </div>);
}
var StyledSimilarSpectrum = styled_1.default(SimilarSpectrum)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  font-size: ", ";\n"], ["\n  display: flex;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var SpectrumItem = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-radius: 2px;\n  margin: 5px;\n  width: 14px;\n  ", ";\n"], ["\n  border-radius: 2px;\n  margin: 5px;\n  width: 14px;\n  ", ";\n"])), function (p) { return "background-color: " + p.theme.similarity.colors[p.colorIndex] + ";"; });
exports.default = StyledSimilarSpectrum;
var templateObject_1, templateObject_2;
//# sourceMappingURL=similarSpectrum.jsx.map