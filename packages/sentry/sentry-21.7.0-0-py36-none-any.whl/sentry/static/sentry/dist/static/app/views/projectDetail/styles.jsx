Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionHeadingLink = exports.SectionHeadingWrapper = exports.SidebarSection = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.SidebarSection = styled_1.default('section')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n\n  ", " {\n    line-height: 1;\n  }\n"], ["\n  margin-bottom: ", ";\n\n  ", " {\n    line-height: 1;\n  }\n"])), space_1.default(2), styles_1.SectionHeading);
exports.SectionHeadingWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
exports.SectionHeadingLink = styled_1.default(globalSelectionLink_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=styles.jsx.map