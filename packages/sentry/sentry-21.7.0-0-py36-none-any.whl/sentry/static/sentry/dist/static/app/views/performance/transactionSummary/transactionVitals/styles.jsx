Object.defineProperty(exports, "__esModule", { value: true });
exports.StatNumber = exports.Description = exports.CardSectionHeading = exports.CardSummary = exports.CardSection = exports.Card = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.Card = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 325px minmax(100px, auto);\n  padding: 0;\n"], ["\n  display: grid;\n  grid-template-columns: 325px minmax(100px, auto);\n  padding: 0;\n"])));
exports.CardSection = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(3));
exports.CardSummary = styled_1.default(exports.CardSection)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  border-right: 1px solid ", ";\n  grid-column: 1/1;\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n"], ["\n  position: relative;\n  border-right: 1px solid ", ";\n  grid-column: 1/1;\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n"])), function (p) { return p.theme.border; });
exports.CardSectionHeading = styled_1.default(styles_1.SectionHeading)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0px;\n"], ["\n  margin: 0px;\n"])));
exports.Description = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
exports.StatNumber = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: 32px;\n"], ["\n  font-size: 32px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=styles.jsx.map