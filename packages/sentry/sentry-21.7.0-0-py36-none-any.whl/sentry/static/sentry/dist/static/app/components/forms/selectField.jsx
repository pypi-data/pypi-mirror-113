Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/utils");
var form_1 = require("./form");
var formField_1 = tslib_1.__importDefault(require("./formField"));
var selectControl_1 = tslib_1.__importDefault(require("./selectControl"));
var SelectField = /** @class */ (function (_super) {
    tslib_1.__extends(SelectField, _super);
    function SelectField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (opt) {
            // Changing this will most likely break react-select (e.g. you won't be able to select
            // a menu option that is from an async request, or a multi select).
            _this.setValue(opt);
        };
        return _this;
    }
    SelectField.prototype.UNSAFE_componentWillReceiveProps = function (nextProps, nextContext) {
        var newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || utils_1.defined(nextContext.form)) {
            var newValue = this.getValue(nextProps, nextContext);
            // This is the only thing that is different from parent, we compare newValue against coerced value in state
            // To remain compatible with react-select, we need to store the option object that
            // includes `value` and `label`, but when we submit the format, we need to coerce it
            // to just return `value`. Also when field changes, it propagates the coerced value up
            var coercedValue = this.coerceValue(this.state.value);
            // newValue can be empty string because of `getValue`, while coerceValue needs to return null (to differentiate
            // empty string from cleared item). We could use `!=` to compare, but lets be a bit more explicit with strict equality
            //
            // This can happen when this is apart of a field, and it re-renders onChange for a different field,
            // there will be a mismatch between this component's state.value and `this.getValue` result above
            if (newValue !== coercedValue && !!newValue !== !!coercedValue) {
                this.setValue(newValue);
            }
        }
    };
    // Overriding this so that we can support `multi` fields through property
    SelectField.prototype.getValue = function (props, context) {
        var form = (context || this.context || {}).form;
        props = props || this.props;
        // Don't use `isMultiple` here because we're taking props from args as well
        var defaultValue = this.isMultiple(props) ? [] : '';
        if (utils_1.defined(props.value)) {
            return props.value;
        }
        if (form && form.data.hasOwnProperty(props.name)) {
            return utils_1.defined(form.data[props.name]) ? form.data[props.name] : defaultValue;
        }
        return utils_1.defined(props.defaultValue) ? props.defaultValue : defaultValue;
    };
    // We need this to get react-select's `Creatable` to work properly
    // Otherwise, when you hit "enter" to create a new item, the "selected value" does
    // not update with new value (and also new value is not displayed in dropdown)
    //
    // This is also needed to get `multi` select working since we need the {label, value} object
    // for react-select (but forms expect just the value to be propagated)
    SelectField.prototype.coerceValue = function (value) {
        if (!value) {
            return '';
        }
        if (this.isMultiple()) {
            return value.map(function (v) { return v.value; });
        }
        else if (value.hasOwnProperty('value')) {
            return value.value;
        }
        return value;
    };
    SelectField.prototype.isMultiple = function (props) {
        props = props || this.props;
        // this is to maintain compatibility with the 'multi' prop
        return props.multi || props.multiple;
    };
    SelectField.prototype.getClassName = function () {
        return '';
    };
    SelectField.prototype.getField = function () {
        var _a = this.props, options = _a.options, clearable = _a.clearable, creatable = _a.creatable, choices = _a.choices, placeholder = _a.placeholder, disabled = _a.disabled, required = _a.required, name = _a.name, isLoading = _a.isLoading;
        return (<StyledSelectControl creatable={creatable} id={this.getId()} choices={choices} options={options} placeholder={placeholder} disabled={disabled} required={required} value={this.state.value} onChange={this.onChange} clearable={clearable} multiple={this.isMultiple()} name={name} isLoading={isLoading}/>);
    };
    SelectField.defaultProps = tslib_1.__assign(tslib_1.__assign({}, formField_1.default.defaultProps), { clearable: true, multiple: false });
    return SelectField;
}(formField_1.default));
exports.default = SelectField;
// This is to match other fields that are wrapped by a `div.control-group`
var StyledSelectControl = styled_1.default(selectControl_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", " &, .form-stacked & {\n    .control-group & {\n      margin-bottom: 0;\n    }\n\n    margin-bottom: 15px;\n  }\n"], ["\n  ", " &, .form-stacked & {\n    .control-group & {\n      margin-bottom: 0;\n    }\n\n    margin-bottom: 15px;\n  }\n"])), form_1.StyledForm);
var templateObject_1;
//# sourceMappingURL=selectField.jsx.map