Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var utils_1 = require("app/utils");
function NotAvailable(_a) {
    var tooltip = _a.tooltip;
    return (<Wrapper>
      <tooltip_1.default title={tooltip} disabled={!utils_1.defined(tooltip)}>
        {'\u2014'}
      </tooltip_1.default>
    </Wrapper>);
}
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray200; });
exports.default = NotAvailable;
var templateObject_1;
//# sourceMappingURL=notAvailable.jsx.map