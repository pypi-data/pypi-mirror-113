Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/utils");
var MultipleCheckboxWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var Label = styled_1.default('label')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n  white-space: nowrap;\n  margin-right: 10px;\n  margin-bottom: 10px;\n  width: 20%;\n"], ["\n  font-weight: normal;\n  white-space: nowrap;\n  margin-right: 10px;\n  margin-bottom: 10px;\n  width: 20%;\n"])));
var CheckboxLabel = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: 3px;\n"], ["\n  margin-left: 3px;\n"])));
var MultipleCheckbox = /** @class */ (function (_super) {
    tslib_1.__extends(MultipleCheckbox, _super);
    function MultipleCheckbox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (selectedValue, e) {
            var _a = _this.props, value = _a.value, onChange = _a.onChange;
            var newValue = [];
            if (typeof onChange !== 'function') {
                return;
            }
            if (e.target.checked) {
                newValue = value ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(value)), [selectedValue]) : [value];
            }
            else {
                newValue = value.filter(function (v) { return v !== selectedValue; });
            }
            onChange(newValue, e);
        };
        return _this;
    }
    MultipleCheckbox.prototype.render = function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, choices = _a.choices, value = _a.value;
        return (<MultipleCheckboxWrapper>
        {choices.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), choiceValue = _b[0], choiceLabel = _b[1];
                return (<LabelContainer key={choiceValue}>
            <Label>
              <input type="checkbox" value={choiceValue} onChange={_this.onChange.bind(_this, choiceValue)} disabled={disabled} checked={utils_1.defined(value) && value.indexOf(choiceValue) !== -1}/>
              <CheckboxLabel>{choiceLabel}</CheckboxLabel>
            </Label>
          </LabelContainer>);
            })}
      </MultipleCheckboxWrapper>);
    };
    return MultipleCheckbox;
}(React.Component));
exports.default = MultipleCheckbox;
var LabelContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  @media (min-width: ", ") {\n    width: 33.333%;\n  }\n  @media (min-width: ", ") {\n    width: 25%;\n  }\n"], ["\n  width: 100%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  @media (min-width: ", ") {\n    width: 33.333%;\n  }\n  @media (min-width: ", ") {\n    width: 25%;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=multipleCheckbox.jsx.map