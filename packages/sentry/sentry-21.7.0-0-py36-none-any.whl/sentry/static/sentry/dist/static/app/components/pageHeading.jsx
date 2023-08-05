Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var PageHeading = styled_1.default('h1')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: ", ";\n  font-weight: normal;\n  margin: 0;\n  margin-bottom: ", ";\n  margin-top: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: ", ";\n  font-weight: normal;\n  margin: 0;\n  margin-bottom: ", ";\n  margin-top: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.headerFontSize; }, function (p) { return p.withMargins && space_1.default(3); }, function (p) { return p.withMargins && space_1.default(1); });
exports.default = PageHeading;
var templateObject_1;
//# sourceMappingURL=pageHeading.jsx.map