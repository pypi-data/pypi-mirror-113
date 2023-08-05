Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var formField_1 = tslib_1.__importDefault(require("app/components/forms/formField"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var utils_1 = require("app/utils");
var MultipleCheckboxField = /** @class */ (function (_super) {
    tslib_1.__extends(MultipleCheckboxField, _super);
    function MultipleCheckboxField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (e, _value) {
            var value = _value; // Casting here to allow _value to be optional, which it has to be since it's overloaded.
            var allValues = _this.state.values;
            if (e.target.checked) {
                if (allValues) {
                    allValues = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(allValues)), [value]);
                }
                else {
                    allValues = [value];
                }
            }
            else {
                allValues = allValues.filter(function (v) { return v !== value; });
            }
            _this.setValues(allValues);
        };
        return _this;
    }
    MultipleCheckboxField.prototype.setValues = function (values) {
        var _this = this;
        var form = (this.context || {}).form;
        this.setState({
            values: values,
        }, function () {
            var finalValue = _this.coerceValue(_this.state.values);
            _this.props.onChange && _this.props.onChange(finalValue);
            form && form.onFieldChange(_this.props.name, finalValue);
        });
    };
    MultipleCheckboxField.prototype.render = function () {
        var _this = this;
        var _a = this.props, required = _a.required, className = _a.className, disabled = _a.disabled, disabledReason = _a.disabledReason, label = _a.label, help = _a.help, choices = _a.choices, hideLabelDivider = _a.hideLabelDivider, style = _a.style;
        var error = this.state.error;
        var cx = classnames_1.default(className, 'control-group', {
            'has-error': error,
        });
        // Hacky, but this isn't really a form label vs the checkbox labels, but
        // we want to treat it as one (i.e. for "required" indicator)
        var labelCx = classnames_1.default({
            required: required,
        });
        var shouldShowDisabledReason = disabled && disabledReason;
        return (<div style={style} className={cx}>
        <div className={labelCx}>
          <div className="controls">
            <label className="control-label" style={{
                display: 'block',
                marginBottom: !hideLabelDivider ? 10 : undefined,
                borderBottom: !hideLabelDivider ? '1px solid #f1eff3' : undefined,
            }}>
              {label}
              {shouldShowDisabledReason && (<tooltip_1.default title={disabledReason}>
                  <span className="disabled-indicator">
                    <icons_1.IconQuestion size="xs"/>
                  </span>
                </tooltip_1.default>)}
            </label>
            {help && <p className="help-block">{help}</p>}
            {error && <p className="error">{error}</p>}
          </div>
        </div>

        <div className="control-list">
          {choices.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), value = _b[0], choiceLabel = _b[1];
                return (<label className="checkbox" key={value}>
              <input type="checkbox" value={value} onChange={function (e) { return _this.onChange(e, value); }} disabled={disabled} checked={utils_1.defined(_this.state.values) && _this.state.values.indexOf(value) !== -1}/>
              {choiceLabel}
            </label>);
            })}
        </div>
      </div>);
    };
    return MultipleCheckboxField;
}(formField_1.default));
exports.default = MultipleCheckboxField;
//# sourceMappingURL=multipleCheckboxField.jsx.map