Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ArrayValue = /** @class */ (function (_super) {
    tslib_1.__extends(ArrayValue, _super);
    function ArrayValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            expanded: false,
        };
        _this.handleToggle = function () {
            _this.setState(function (prevState) { return ({
                expanded: !prevState.expanded,
            }); });
        };
        return _this;
    }
    ArrayValue.prototype.render = function () {
        var expanded = this.state.expanded;
        var value = this.props.value;
        return (<ArrayContainer expanded={expanded}>
        {expanded &&
                value
                    .slice(0, value.length - 1)
                    .map(function (item, i) { return <ArrayItem key={i + ":" + item}>{item}</ArrayItem>; })}
        <ArrayItem>{value.slice(-1)[0]}</ArrayItem>
        {value.length > 1 ? (<ButtonContainer>
            <button onClick={this.handleToggle}>
              {expanded ? locale_1.t('[collapse]') : locale_1.t('[+%s more]', value.length - 1)}
            </button>
          </ButtonContainer>) : null}
      </ArrayContainer>);
    };
    return ArrayValue;
}(react_1.Component));
var ArrayContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: ", ";\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n    cursor: pointer;\n    color: ", ";\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: ", ";\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n    cursor: pointer;\n    color: ", ";\n    margin-left: ", ";\n  }\n"])), function (p) { return (p.expanded ? 'column' : 'row'); }, function (p) { return p.theme.blue300; }, space_1.default(0.5));
var ArrayItem = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  display: block;\n\n  ", ";\n  width: unset;\n"], ["\n  flex-shrink: 1;\n  display: block;\n\n  ", ";\n  width: unset;\n"])), overflowEllipsis_1.default);
var ButtonContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
exports.default = ArrayValue;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=arrayValue.jsx.map