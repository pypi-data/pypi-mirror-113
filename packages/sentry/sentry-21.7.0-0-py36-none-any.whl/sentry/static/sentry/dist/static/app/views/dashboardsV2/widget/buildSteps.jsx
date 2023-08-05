Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function BuildSteps(_a) {
    var children = _a.children;
    return <StyledList symbol="colored-numeric">{children}</StyledList>;
}
exports.default = BuildSteps;
var StyledList = styled_1.default(list_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  max-width: 100%;\n\n  @media (min-width: ", ") {\n    max-width: 50%;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  max-width: 100%;\n\n  @media (min-width: ", ") {\n    max-width: 50%;\n  }\n"])), space_1.default(4), function (p) { return p.theme.breakpoints[4]; });
var templateObject_1;
//# sourceMappingURL=buildSteps.jsx.map