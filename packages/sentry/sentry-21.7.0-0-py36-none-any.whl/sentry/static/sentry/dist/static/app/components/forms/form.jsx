Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledForm = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var formContext_1 = tslib_1.__importDefault(require("app/components/forms/formContext"));
var state_1 = tslib_1.__importDefault(require("app/components/forms/state"));
var locale_1 = require("app/locale");
var Form = /** @class */ (function (_super) {
    tslib_1.__extends(Form, _super);
    function Form(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.onSubmit = function (e) {
            e.preventDefault();
            if (!_this.props.onSubmit) {
                throw new Error('onSubmit is a required prop');
            }
            _this.props.onSubmit(_this.state.data, _this.onSubmitSuccess, _this.onSubmitError);
        };
        _this.onSubmitSuccess = function (data) {
            _this.setState({
                state: state_1.default.READY,
                errors: {},
                initialData: tslib_1.__assign(tslib_1.__assign({}, _this.state.data), (data || {})),
            });
            _this.props.onSubmitSuccess && _this.props.onSubmitSuccess(data);
        };
        _this.onSubmitError = function (error) {
            _this.setState({
                state: state_1.default.ERROR,
                errors: error.responseJSON,
            });
            if (_this.props.resetOnError) {
                _this.setState({
                    initialData: {},
                });
            }
            _this.props.onSubmitError && _this.props.onSubmitError(error);
        };
        _this.onFieldChange = function (name, value) {
            _this.setState(function (state) {
                var _a;
                return ({
                    data: tslib_1.__assign(tslib_1.__assign({}, state.data), (_a = {}, _a[name] = value, _a)),
                });
            });
        };
        _this.state = {
            data: tslib_1.__assign({}, _this.props.initialData),
            errors: {},
            initialData: tslib_1.__assign({}, _this.props.initialData),
            state: state_1.default.READY,
        };
        return _this;
    }
    Form.prototype.getContext = function () {
        var _a = this.state, data = _a.data, errors = _a.errors;
        return {
            form: {
                data: data,
                errors: errors,
                onFieldChange: this.onFieldChange,
            },
        };
    };
    Form.prototype.render = function () {
        var isSaving = this.state.state === state_1.default.SAVING;
        var _a = this.state, initialData = _a.initialData, data = _a.data;
        var _b = this.props, errorMessage = _b.errorMessage, hideErrors = _b.hideErrors, requireChanges = _b.requireChanges;
        var hasChanges = requireChanges
            ? Object.keys(data).length && !isEqual_1.default(data, initialData)
            : true;
        var isError = this.state.state === state_1.default.ERROR;
        var nonFieldErrors = this.state.errors && this.state.errors.non_field_errors;
        return (<formContext_1.default.Provider value={this.getContext()}>
        <exports.StyledForm onSubmit={this.onSubmit} className={this.props.className}>
          {isError && !hideErrors && (<div className="alert alert-error alert-block">
              {nonFieldErrors ? (<div>
                  <p>
                    {locale_1.t('Unable to save your changes. Please correct the following errors try again.')}
                  </p>
                  <ul>
                    {nonFieldErrors.map(function (e, i) { return (<li key={i}>{e}</li>); })}
                  </ul>
                </div>) : (errorMessage)}
            </div>)}
          {this.props.children}
          <div className={this.props.footerClass} style={{ marginTop: 25 }}>
            <button className="btn btn-primary" disabled={isSaving || this.props.submitDisabled || !hasChanges} type="submit">
              {this.props.submitLabel}
            </button>
            {this.props.onCancel && (<button type="button" className="btn btn-default" disabled={isSaving} onClick={this.props.onCancel} style={{ marginLeft: 5 }}>
                {this.props.cancelLabel}
              </button>)}
            {this.props.extraButton}
          </div>
        </exports.StyledForm>
      </formContext_1.default.Provider>);
    };
    Form.defaultProps = {
        cancelLabel: locale_1.t('Cancel'),
        submitLabel: locale_1.t('Save Changes'),
        submitDisabled: false,
        footerClass: 'form-actions align-right',
        className: 'form-stacked',
        requireChanges: false,
        hideErrors: false,
        resetOnError: false,
        errorMessage: locale_1.t('Unable to save your changes. Please ensure all fields are valid and try again.'),
    };
    return Form;
}(React.Component));
// Note: this is so we can use this as a selector for SelectField
// We need to keep `Form` as a React Component because ApiForm extends it :/
exports.StyledForm = styled_1.default('form')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
exports.default = Form;
var templateObject_1;
//# sourceMappingURL=form.jsx.map