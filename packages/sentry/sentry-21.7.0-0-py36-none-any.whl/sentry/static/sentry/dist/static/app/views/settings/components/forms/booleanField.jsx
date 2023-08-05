Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var BooleanField = /** @class */ (function (_super) {
    tslib_1.__extends(BooleanField, _super);
    function BooleanField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (value, onChange, onBlur, e) {
            // We need to toggle current value because Switch is not an input
            var newValue = _this.coerceValue(!value);
            onChange(newValue, e);
            onBlur(newValue, e);
        };
        return _this;
    }
    BooleanField.prototype.coerceValue = function (value) {
        return !!value;
    };
    BooleanField.prototype.render = function () {
        var _this = this;
        var _a = this.props, confirm = _a.confirm, fieldProps = tslib_1.__rest(_a, ["confirm"]);
        return (<inputField_1.default {...fieldProps} resetOnError field={function (_a) {
                var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, disabled = _a.disabled, props = tslib_1.__rest(_a, ["onChange", "onBlur", "value", "disabled"]);
                // Create a function with required args bound
                var handleChange = _this.handleChange.bind(_this, value, onChange, onBlur);
                var switchProps = tslib_1.__assign(tslib_1.__assign({}, props), { size: 'lg', isActive: !!value, isDisabled: disabled, toggle: handleChange });
                if (confirm) {
                    return (<confirm_1.default renderMessage={function () { return confirm[(!value).toString()]; }} onConfirm={function () { return handleChange({}); }}>
                {function (_a) {
                            var open = _a.open;
                            return (<switchButton_1.default {...switchProps} toggle={function (e) {
                                    // If we have a `confirm` prop and enabling switch
                                    // Then show confirm dialog, otherwise propagate change as normal
                                    if (confirm[(!value).toString()]) {
                                        // Open confirm modal
                                        open();
                                        return;
                                    }
                                    handleChange(e);
                                }}/>);
                        }}
              </confirm_1.default>);
                }
                return <switchButton_1.default {...switchProps}/>;
            }}/>);
    };
    return BooleanField;
}(React.Component));
exports.default = BooleanField;
//# sourceMappingURL=booleanField.jsx.map