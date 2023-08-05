Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SourceSuggestionExamples = function (_a) {
    var examples = _a.examples, sourceName = _a.sourceName;
    return (<Wrapper>
    <ExampleCard position="right" header={locale_1.t('Examples for %s in current event', <code>{sourceName}</code>)} body={examples.map(function (example) { return (<pre key={example}>{example}</pre>); })}>
      <Content>
        {locale_1.t('See Example')} <icons_1.IconQuestion size="xs"/>
      </Content>
    </ExampleCard>
  </Wrapper>);
};
exports.default = SourceSuggestionExamples;
var ExampleCard = styled_1.default(hovercard_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 400px;\n\n  pre:last-child {\n    margin: 0;\n  }\n"], ["\n  width: 400px;\n\n  pre:last-child {\n    margin: 0;\n  }\n"])));
var Content = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n  text-decoration: underline;\n  text-decoration-style: dotted;\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n  text-decoration: underline;\n  text-decoration-style: dotted;\n"])), space_1.default(0.5), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeSmall; });
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-column: 3/3;\n"], ["\n  grid-column: 3/3;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sourceSuggestionExamples.jsx.map