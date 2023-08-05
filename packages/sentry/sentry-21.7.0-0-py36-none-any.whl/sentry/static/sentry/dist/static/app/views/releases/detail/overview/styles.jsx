Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionHeading = exports.Wrapper = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.SectionHeading = styled_1.default(styles_1.SectionHeading)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0 0 ", " 0;\n"], ["\n  margin: 0 0 ", " 0;\n"])), space_1.default(1.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map