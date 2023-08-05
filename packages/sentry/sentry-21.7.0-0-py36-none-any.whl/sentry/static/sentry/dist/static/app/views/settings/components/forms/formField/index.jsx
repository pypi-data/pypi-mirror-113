Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var mobx_react_1 = require("mobx-react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var panelAlert_1 = tslib_1.__importDefault(require("app/components/panels/panelAlert"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var sanitizeQuerySelector_1 = require("app/utils/sanitizeQuerySelector");
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var fieldControl_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldControl"));
var fieldErrorReason_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldErrorReason"));
var formContext_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formContext"));
var controlState_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField/controlState"));
var model_1 = require("app/views/settings/components/forms/model");
var returnButton_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/returnButton"));
/**
 * Some fields don't need to implement their own onChange handlers, in
 * which case we will receive an Event, but if they do we should handle
 * the case where they return a value as the first argument.
 */
var getValueFromEvent = function (valueOrEvent, e) {
    var _a;
    var event = e || valueOrEvent;
    var value = utils_1.defined(e) ? valueOrEvent : (_a = event === null || event === void 0 ? void 0 : event.target) === null || _a === void 0 ? void 0 : _a.value;
    return { value: value, event: event };
};
/**
 * This is a list of field properties that can accept a function taking the
 * form model, that will be called to determine the value of the prop upon an
 * observed change in the model.
 *
 * This uses mobx's observation of the models observable fields.
 */
var propsToObserver = ['help', 'inline', 'highlighted', 'visible', 'disabled'];
var FormField = /** @class */ (function (_super) {
    tslib_1.__extends(FormField, _super);
    function FormField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.input = null;
        /**
         * Attempts to autofocus input field if field's name is in url hash.
         *
         * The ref must be forwared for this to work.
         */
        _this.handleInputMount = function (node) {
            var _a;
            if (node && !_this.input) {
                // TODO(mark) Clean this up. FormContext could include the location
                var hash = (_a = window.location) === null || _a === void 0 ? void 0 : _a.hash;
                if (!hash) {
                    return;
                }
                if (hash !== "#" + _this.props.name) {
                    return;
                }
                // Not all form fields have this (e.g. Select fields)
                if (typeof node.focus === 'function') {
                    node.focus();
                }
            }
            _this.input = node;
        };
        /**
         * Update field value in form model
         */
        _this.handleChange = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, name = _a.name, onChange = _a.onChange;
            var _b = getValueFromEvent.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args))), value = _b.value, event = _b.event;
            var model = _this.getModel();
            if (onChange) {
                onChange(value, event);
            }
            model.setValue(name, value);
        };
        /**
         * Notify model of a field being blurred
         */
        _this.handleBlur = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, name = _a.name, onBlur = _a.onBlur;
            var _b = getValueFromEvent.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args))), value = _b.value, event = _b.event;
            var model = _this.getModel();
            if (onBlur) {
                onBlur(value, event);
            }
            // Always call this, so model can decide what to do
            model.handleBlurField(name, value);
        };
        /**
         * Handle keydown to trigger a save on Enter
         */
        _this.handleKeyDown = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, onKeyDown = _a.onKeyDown, name = _a.name;
            var _b = getValueFromEvent.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args))), value = _b.value, event = _b.event;
            var model = _this.getModel();
            if (event.key === 'Enter') {
                model.handleBlurField(name, value);
            }
            if (onKeyDown) {
                onKeyDown(value, event);
            }
        };
        /**
         * Handle saving an individual field via UI button
         */
        _this.handleSaveField = function () {
            var name = _this.props.name;
            var model = _this.getModel();
            model.handleSaveField(name, model.getValue(name));
        };
        _this.handleCancelField = function () {
            var name = _this.props.name;
            var model = _this.getModel();
            model.handleCancelSaveField(name);
        };
        return _this;
    }
    FormField.prototype.componentDidMount = function () {
        // Tell model about this field's props
        this.getModel().setFieldDescriptor(this.props.name, this.props);
    };
    FormField.prototype.componentWillUnmount = function () {
        this.getModel().removeField(this.props.name);
    };
    FormField.prototype.getError = function () {
        return this.getModel().getError(this.props.name);
    };
    FormField.prototype.getId = function () {
        return sanitizeQuerySelector_1.sanitizeQuerySelector(this.props.name);
    };
    FormField.prototype.getModel = function () {
        return this.context.form !== undefined
            ? this.context.form
            : new model_1.MockModel(this.props);
    };
    FormField.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, name = _a.name, hideErrorMessage = _a.hideErrorMessage, flexibleControlStateSize = _a.flexibleControlStateSize, saveOnBlur = _a.saveOnBlur, saveMessage = _a.saveMessage, saveMessageAlertType = _a.saveMessageAlertType, selectionInfoFunction = _a.selectionInfoFunction, hideControlState = _a.hideControlState, 
        // Don't pass `defaultValue` down to input fields, will be handled in
        // form model
        _defaultValue = _a.defaultValue, otherProps = tslib_1.__rest(_a, ["className", "name", "hideErrorMessage", "flexibleControlStateSize", "saveOnBlur", "saveMessage", "saveMessageAlertType", "selectionInfoFunction", "hideControlState", "defaultValue"]);
        var id = this.getId();
        var model = this.getModel();
        var saveOnBlurFieldOverride = typeof saveOnBlur !== 'undefined' && !saveOnBlur;
        var makeField = function (resolvedObservedProps) {
            var props = tslib_1.__assign(tslib_1.__assign({}, otherProps), resolvedObservedProps);
            return (<React.Fragment>
          <field_1.default id={id} className={className} flexibleControlStateSize={flexibleControlStateSize} {...props}>
            {function (_a) {
                    var alignRight = _a.alignRight, inline = _a.inline, disabled = _a.disabled, disabledReason = _a.disabledReason;
                    return (<fieldControl_1.default disabled={disabled} disabledReason={disabledReason} inline={inline} alignRight={alignRight} flexibleControlStateSize={flexibleControlStateSize} hideControlState={hideControlState} controlState={<controlState_1.default model={model} name={name}/>} errorState={<mobx_react_1.Observer>
                    {function () {
                                var error = _this.getError();
                                var shouldShowErrorMessage = error && !hideErrorMessage;
                                if (!shouldShowErrorMessage) {
                                    return null;
                                }
                                return <fieldErrorReason_1.default>{error}</fieldErrorReason_1.default>;
                            }}
                  </mobx_react_1.Observer>}>
                <mobx_react_1.Observer>
                  {function () {
                            var error = _this.getError();
                            var value = model.getValue(name);
                            var showReturnButton = model.getFieldState(name, 'showReturnButton');
                            return (<React.Fragment>
                        {_this.props.children(tslib_1.__assign(tslib_1.__assign({ ref: _this.handleInputMount }, props), { model: model, name: name, id: id, onKeyDown: _this.handleKeyDown, onChange: _this.handleChange, onBlur: _this.handleBlur, 
                                    // Fixes react warnings about input switching from controlled to uncontrolled
                                    // So force to empty string for null values
                                    value: value === null ? '' : value, error: error, disabled: disabled, initialData: model.initialData }))}
                        {showReturnButton && <StyledReturnButton />}
                      </React.Fragment>);
                        }}
                </mobx_react_1.Observer>
              </fieldControl_1.default>);
                }}
          </field_1.default>
          {selectionInfoFunction && (<mobx_react_1.Observer>
              {function () {
                        var error = _this.getError();
                        var value = model.getValue(name);
                        var isVisible = typeof props.visible === 'function'
                            ? props.visible(tslib_1.__assign(tslib_1.__assign({}, _this.props), props))
                            : true;
                        return (<React.Fragment>
                    {isVisible ? selectionInfoFunction(tslib_1.__assign(tslib_1.__assign({}, props), { error: error, value: value })) : null}
                  </React.Fragment>);
                    }}
            </mobx_react_1.Observer>)}
          {saveOnBlurFieldOverride && (<mobx_react_1.Observer>
              {function () {
                        var showFieldSave = model.getFieldState(name, 'showSave');
                        var value = model.getValue(name);
                        if (!showFieldSave) {
                            return null;
                        }
                        return (<panelAlert_1.default type={saveMessageAlertType}>
                    <MessageAndActions>
                      <div>
                        {typeof saveMessage === 'function'
                                ? saveMessage(tslib_1.__assign(tslib_1.__assign({}, props), { value: value }))
                                : saveMessage}
                      </div>
                      <buttonBar_1.default gap={1}>
                        <button_1.default onClick={_this.handleCancelField}>{locale_1.t('Cancel')}</button_1.default>
                        <button_1.default priority="primary" type="button" onClick={_this.handleSaveField}>
                          {locale_1.t('Save')}
                        </button_1.default>
                      </buttonBar_1.default>
                    </MessageAndActions>
                  </panelAlert_1.default>);
                    }}
            </mobx_react_1.Observer>)}
        </React.Fragment>);
        };
        var observedProps = propsToObserver
            .filter(function (p) { return typeof _this.props[p] === 'function'; })
            .map(function (p) { return [
            p,
            function () { return _this.props[p](tslib_1.__assign(tslib_1.__assign({}, _this.props), { model: model })); },
        ]; });
        // This field has no properties that require observation to compute their
        // value, this field is static and will not be re-rendered.
        if (observedProps.length === 0) {
            return makeField();
        }
        var resolveObservedProps = function (props, _a) {
            var _b;
            var _c = tslib_1.__read(_a, 2), propName = _c[0], resolve = _c[1];
            return (tslib_1.__assign(tslib_1.__assign({}, props), (_b = {}, _b[propName] = resolve(), _b)));
        };
        return (<mobx_react_1.Observer>
        {function () { return makeField(observedProps.reduce(resolveObservedProps, {})); }}
      </mobx_react_1.Observer>);
    };
    FormField.defaultProps = {
        hideErrorMessage: false,
        flexibleControlStateSize: false,
    };
    FormField.contextType = formContext_1.default;
    return FormField;
}(React.Component));
exports.default = FormField;
var MessageAndActions = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(2));
var StyledReturnButton = styled_1.default(returnButton_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  right: 0;\n  top: 0;\n"], ["\n  position: absolute;\n  right: 0;\n  top: 0;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map