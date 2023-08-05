Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ListItem = styled_1.default(function (_a) {
    var children = _a.children, className = _a.className, symbol = _a.symbol, onClick = _a.onClick;
    return (<li className={className} onClick={onClick}>
    {symbol && <Symbol>{symbol}</Symbol>}
    {children}
  </li>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  ", "\n"], ["\n  position: relative;\n  ", "\n"])), function (p) { return p.symbol && "padding-left: " + space_1.default(4) + ";"; });
var Symbol = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: absolute;\n  top: 0;\n  left: 0;\n  min-height: 22.5px;\n"], ["\n  display: flex;\n  align-items: center;\n  position: absolute;\n  top: 0;\n  left: 0;\n  min-height: 22.5px;\n"])));
exports.default = ListItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=listItem.jsx.map