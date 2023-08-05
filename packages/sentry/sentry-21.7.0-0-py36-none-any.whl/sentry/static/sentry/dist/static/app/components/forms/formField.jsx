Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var formContext_1 = tslib_1.__importDefault(require("app/components/forms/formContext"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var utils_1 = require("app/utils");
var FormField = /** @class */ (function (_super) {
    tslib_1.__extends(FormField, _super);
    function FormField(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.onChange = function (e) {
            var value = e.target.value;
            _this.setValue(value);
        };
        _this.setValue = function (value) {
            var form = (_this.context || {}).form;
            _this.setState({
                value: value,
            }, function () {
                var _a, _b;
                var finalValue = _this.coerceValue(_this.state.value);
                (_b = (_a = _this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, finalValue);
                form === null || form === void 0 ? void 0 : form.onFieldChange(_this.props.name, finalValue);
            });
        };
        _this.state = {
            error: null,
            value: _this.getValue(props, context),
        };
        return _this;
    }
    FormField.prototype.componentDidMount = function () { };
    FormField.prototype.UNSAFE_componentWillReceiveProps = function (nextProps, nextContext) {
        var newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || utils_1.defined(nextContext.form)) {
            var newValue = this.getValue(nextProps, nextContext);
            if (newValue !== this.state.value) {
                this.setValue(newValue);
            }
        }
    };
    FormField.prototype.componentWillUnmount = function () { };
    FormField.prototype.getValue = function (props, context) {
        var form = (context || this.context || {}).form;
        props = props || this.props;
        if (utils_1.defined(props.value)) {
            return props.value;
        }
        if (form && form.data.hasOwnProperty(props.name)) {
            return utils_1.defined(form.data[props.name]) ? form.data[props.name] : '';
        }
        return utils_1.defined(props.defaultValue) ? props.defaultValue : '';
    };
    FormField.prototype.getError = function (props, context) {
        var form = (context || this.context || {}).form;
        props = props || this.props;
        if (utils_1.defined(props.error)) {
            return props.error;
        }
        return (form && form.errors[props.name]) || null;
    };
    FormField.prototype.getId = function () {
        return "id-" + this.props.name;
    };
    FormField.prototype.coerceValue = function (value) {
        return value;
    };
    FormField.prototype.getField = function () {
        throw new Error('Must be implemented by child.');
    };
    FormField.prototype.getClassName = function () {
        throw new Error('Must be implemented by child.');
    };
    FormField.prototype.getFinalClassNames = function () {
        var _a = this.props, className = _a.className, required = _a.required;
        var error = this.state.error;
        return classnames_1.default(className, this.getClassName(), {
            'has-error': !!error,
            required: required,
        });
    };
    FormField.prototype.renderDisabledReason = function () {
        var _a = this.props, disabled = _a.disabled, disabledReason = _a.disabledReason;
        if (!disabled) {
            return null;
        }
        if (!disabledReason) {
            return null;
        }
        return <questionTooltip_1.default title={disabledReason} position="top" size="sm"/>;
    };
    FormField.prototype.render = function () {
        var _a = this.props, label = _a.label, hideErrorMessage = _a.hideErrorMessage, help = _a.help, style = _a.style;
        var error = this.state.error;
        var cx = this.getFinalClassNames();
        var shouldShowErrorMessage = error && !hideErrorMessage;
        return (<div style={style} className={cx}>
        <div className="controls">
          {label && (<label htmlFor={this.getId()} className="control-label">
              {label}
            </label>)}
          {this.getField()}
          {this.renderDisabledReason()}
          {utils_1.defined(help) && <p className="help-block">{help}</p>}
          {shouldShowErrorMessage && <ErrorMessage>{error}</ErrorMessage>}
        </div>
      </div>);
    };
    FormField.defaultProps = {
        hideErrorMessage: false,
        disabled: false,
        required: false,
    };
    FormField.contextType = formContext_1.default;
    return FormField;
}(React.PureComponent));
exports.default = FormField;
var ErrorMessage = styled_1.default('p')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.red300; });
var templateObject_1;
//# sourceMappingURL=formField.jsx.map