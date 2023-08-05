Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SelectorItem = /** @class */ (function (_super) {
    tslib_1.__extends(SelectorItem, _super);
    function SelectorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function (e) {
            var _a = _this.props, onClick = _a.onClick, value = _a.value;
            onClick(value, e);
        };
        return _this;
    }
    SelectorItem.prototype.render = function () {
        var _a = this.props, className = _a.className, label = _a.label;
        return (<div className={className} onClick={this.handleClick}>
        <Label>{label}</Label>
      </div>);
    };
    return SelectorItem;
}(React.PureComponent));
var StyledSelectorItem = styled_1.default(SelectorItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  cursor: pointer;\n  white-space: nowrap;\n  padding: ", ";\n  align-items: center;\n  flex: 1;\n  background-color: ", ";\n  color: ", ";\n  font-weight: ", ";\n  border-bottom: 1px solid ", ";\n\n  &:hover {\n    color: ", ";\n    background: ", ";\n  }\n"], ["\n  display: flex;\n  cursor: pointer;\n  white-space: nowrap;\n  padding: ", ";\n  align-items: center;\n  flex: 1;\n  background-color: ", ";\n  color: ", ";\n  font-weight: ", ";\n  border-bottom: 1px solid ", ";\n\n  &:hover {\n    color: ", ";\n    background: ", ";\n  }\n"])), space_1.default(1), function (p) { return (p.selected ? p.theme.active : 'transparent'); }, function (p) { return (p.selected ? p.theme.white : p.theme.subText); }, function (p) { return (p.selected ? 'bold' : 'normal'); }, function (p) { return (p.last ? 'transparent' : p.theme.innerBorder); }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.focus; });
var Label = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = StyledSelectorItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=selectorItem.jsx.map