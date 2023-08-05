Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var rangeSlider_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/rangeSlider"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
function onChange(fieldOnChange, value, e) {
    fieldOnChange(value, e);
}
function defaultFormatMessageValue(value, props) {
    return (typeof props.formatLabel === 'function' && props.formatLabel(value)) || value;
}
function RangeField(_a) {
    var _b = _a.formatMessageValue, formatMessageValue = _b === void 0 ? defaultFormatMessageValue : _b, disabled = _a.disabled, otherProps = tslib_1.__rest(_a, ["formatMessageValue", "disabled"]);
    var resolvedDisabled = typeof disabled === 'function' ? disabled(otherProps) : disabled;
    var props = tslib_1.__assign(tslib_1.__assign({}, otherProps), { disabled: resolvedDisabled, formatMessageValue: formatMessageValue });
    return (<inputField_1.default {...props} field={function (_a) {
            var fieldOnChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, fieldProps = tslib_1.__rest(_a, ["onChange", "onBlur", "value"]);
            return (<rangeSlider_1.default {...fieldProps} value={value} onBlur={onBlur} onChange={function (val, event) { return onChange(fieldOnChange, val, event); }}/>);
        }}/>);
}
exports.default = RangeField;
//# sourceMappingURL=rangeField.jsx.map