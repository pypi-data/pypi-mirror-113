Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var utils_1 = require("app/utils");
var BooleanField = /** @class */ (function (_super) {
    tslib_1.__extends(BooleanField, _super);
    function BooleanField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (e) {
            var value = e.target.checked;
            _this.setValue(value);
        };
        return _this;
    }
    BooleanField.prototype.coerceValue = function (initialValue) {
        var value = _super.prototype.coerceValue.call(this, initialValue);
        return value ? true : false;
    };
    BooleanField.prototype.getField = function () {
        return (<input id={this.getId()} type={this.getType()} checked={this.state.value} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>);
    };
    BooleanField.prototype.render = function () {
        var error = this.state.error;
        var className = this.getClassName();
        if (error) {
            className += ' has-error';
        }
        return (<div className={className}>
        <div className="controls">
          <label className="control-label">
            {this.getField()}
            {this.props.label}
            {this.props.disabled && this.props.disabledReason && (<tooltip_1.default title={this.props.disabledReason}>
                <icons_1.IconQuestion size="xs"/>
              </tooltip_1.default>)}
          </label>
          {utils_1.defined(this.props.help) && <p className="help-block">{this.props.help}</p>}
          {error && <p className="error">{error}</p>}
        </div>
      </div>);
    };
    BooleanField.prototype.getClassName = function () {
        return 'control-group checkbox';
    };
    BooleanField.prototype.getType = function () {
        return 'checkbox';
    };
    return BooleanField;
}(inputField_1.default));
exports.default = BooleanField;
//# sourceMappingURL=booleanField.jsx.map