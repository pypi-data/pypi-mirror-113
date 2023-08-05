Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var radioGroup_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/radioGroup"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var RadioField = /** @class */ (function (_super) {
    tslib_1.__extends(RadioField, _super);
    function RadioField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (id, onChange, onBlur, e) {
            onChange(id, e);
            onBlur(id, e);
        };
        return _this;
    }
    RadioField.prototype.render = function () {
        var _this = this;
        return (<inputField_1.default {...this.props} field={function (_a) {
                var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, disabled = _a.disabled, orientInline = _a.orientInline, props = tslib_1.__rest(_a, ["onChange", "onBlur", "value", "disabled", "orientInline"]);
                return (<radioGroup_1.default choices={props.choices} disabled={disabled} orientInline={orientInline} value={value === '' ? null : value} label={props.label} onChange={function (id, e) { return _this.onChange(id, onChange, onBlur, e); }}/>);
            }}/>);
    };
    return RadioField;
}(React.Component));
exports.default = RadioField;
//# sourceMappingURL=radioField.jsx.map