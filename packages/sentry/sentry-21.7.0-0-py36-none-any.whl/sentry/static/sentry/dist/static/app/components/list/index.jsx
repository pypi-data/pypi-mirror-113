Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("./utils");
var List = styled_1.default(function (_a) {
    var children = _a.children, className = _a.className, symbol = _a.symbol, _initialCounterValue = _a.initialCounterValue, props = tslib_1.__rest(_a, ["children", "className", "symbol", "initialCounterValue"]);
    var getWrapperComponent = function () {
        switch (symbol) {
            case 'numeric':
            case 'colored-numeric':
                return 'ol';
            default:
                return 'ul';
        }
    };
    var Wrapper = getWrapperComponent();
    return (<Wrapper className={className} {...props}>
        {!symbol || typeof symbol === 'string'
            ? children
            : React.Children.map(children, function (child) {
                if (!React.isValidElement(child)) {
                    return child;
                }
                return React.cloneElement(child, {
                    symbol: symbol,
                });
            })}
      </Wrapper>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  padding: 0;\n  list-style: none;\n  display: grid;\n  grid-gap: ", ";\n  ", "\n"], ["\n  margin: 0;\n  padding: 0;\n  list-style: none;\n  display: grid;\n  grid-gap: ", ";\n  ", "\n"])), space_1.default(0.5), function (p) {
    return typeof p.symbol === 'string' &&
        utils_1.listSymbol[p.symbol] &&
        utils_1.getListSymbolStyle(p.theme, p.symbol, p.initialCounterValue);
});
exports.default = List;
var templateObject_1;
//# sourceMappingURL=index.jsx.map