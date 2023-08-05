Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
function List(_a) {
    var items = _a.items, className = _a.className;
    if (!items.length) {
        return null;
    }
    return <Wrapper className={className}>{items}</Wrapper>;
}
exports.default = List;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  font-size: ", ";\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=list.jsx.map