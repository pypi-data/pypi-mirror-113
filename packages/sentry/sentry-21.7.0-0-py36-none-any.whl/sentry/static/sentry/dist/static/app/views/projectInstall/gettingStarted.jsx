Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function GettingStarted(_a) {
    var className = _a.className, children = _a.children;
    return <organization_1.PageContent className={className}>{children}</organization_1.PageContent>;
}
exports.default = styled_1.default(GettingStarted)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  padding-top: ", ";\n"], ["\n  background: ", ";\n  padding-top: ", ";\n"])), function (p) { return p.theme.background; }, space_1.default(3));
var templateObject_1;
//# sourceMappingURL=gettingStarted.jsx.map