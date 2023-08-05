Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var progressRing_1 = tslib_1.__importDefault(require("app/components/progressRing"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ProgressHeader = function (_a) {
    var theme = _a.theme, allTasks = _a.allTasks, completedTasks = _a.completedTasks;
    return (<Container>
    <StyledProgressRing size={80} barWidth={8} text={allTasks.length - completedTasks.length} animateText value={(completedTasks.length / allTasks.length) * 100} progressEndcaps="round" backgroundColor={theme.gray100} textCss={function () { return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n        font-size: 26px;\n        color: ", ";\n      "], ["\n        font-size: 26px;\n        color: ", ";\n      "])), theme.textColor); }}/>
    <HeaderTitle>{locale_1.t('Quick Start')}</HeaderTitle>
    <Description>
      {locale_1.t("Take full advantage of Sentry's powerful monitoring features.")}
    </Description>
  </Container>);
};
exports.default = react_1.withTheme(ProgressHeader);
var Container = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content 1fr;\n  grid-template-rows: min-content 1fr;\n  grid-column-gap: ", ";\n  margin: 90px ", " 0 ", ";\n"], ["\n  display: grid;\n  grid-template-columns: min-content 1fr;\n  grid-template-rows: min-content 1fr;\n  grid-column-gap: ", ";\n  margin: 90px ", " 0 ", ";\n"])), space_1.default(2), space_1.default(4), space_1.default(4));
var StyledProgressRing = styled_1.default(progressRing_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/2;\n  grid-row: 1/3;\n"], ["\n  grid-column: 1/2;\n  grid-row: 1/3;\n"])));
var HeaderTitle = styled_1.default('h3')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  grid-column: 2/3;\n  grid-row: 1/2;\n"], ["\n  margin: 0;\n  grid-column: 2/3;\n  grid-row: 1/2;\n"])));
var Description = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  grid-column: 2/3;\n  grid-row: 2/3;\n"], ["\n  color: ", ";\n  grid-column: 2/3;\n  grid-row: 2/3;\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=progressHeader.jsx.map