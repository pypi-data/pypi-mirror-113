Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var utils_1 = require("app/utils");
var RadioBooleanField = /** @class */ (function (_super) {
    tslib_1.__extends(RadioBooleanField, _super);
    function RadioBooleanField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (e) {
            var value = e.target.value === 'true';
            _this.setValue(value);
        };
        return _this;
    }
    RadioBooleanField.prototype.coerceValue = function (props) {
        var value = _super.prototype.coerceValue.call(this, props);
        return value ? true : false;
    };
    RadioBooleanField.prototype.getType = function () {
        return 'radio';
    };
    RadioBooleanField.prototype.getField = function () {
        var yesOption = (<div className="radio" key="yes">
        <label style={{ fontWeight: 'normal' }}>
          <input type="radio" value="true" name={this.props.name} checked={this.state.value === true} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>{' '}
          {this.props.yesLabel}
        </label>
      </div>);
        var noOption = (<div className="radio" key="no">
        <label style={{ fontWeight: 'normal' }}>
          <input type="radio" name={this.props.name} value="false" checked={this.state.value === false} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>{' '}
          {this.props.noLabel}
        </label>
      </div>);
        return (<div className="control-group radio-boolean">
        {this.props.yesFirst ? (<react_1.Fragment>
            {yesOption}
            {noOption}
          </react_1.Fragment>) : (<react_1.Fragment>
            {noOption}
            {yesOption}
          </react_1.Fragment>)}
      </div>);
    };
    RadioBooleanField.prototype.render = function () {
        var _a = this.props, label = _a.label, hideErrorMessage = _a.hideErrorMessage, help = _a.help, style = _a.style;
        var error = this.state.error;
        var cx = this.getFinalClassNames();
        var shouldShowErrorMessage = error && !hideErrorMessage;
        return (<div style={style} className={cx}>
        <div className="controls">
          {label && (<label htmlFor={this.getId()} className="control-label">
              {label}
            </label>)}
          {utils_1.defined(help) && <p className="help-block">{help}</p>}
          {this.getField()}
          {this.renderDisabledReason()}
          {shouldShowErrorMessage && <p className="error">{error}</p>}
        </div>
      </div>);
    };
    RadioBooleanField.defaultProps = tslib_1.__assign(tslib_1.__assign({}, inputField_1.default.defaultProps), { yesLabel: 'Yes', noLabel: 'No', yesFirst: true });
    return RadioBooleanField;
}(inputField_1.default));
exports.default = RadioBooleanField;
//# sourceMappingURL=radioBooleanField.jsx.map