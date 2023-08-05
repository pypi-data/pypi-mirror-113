Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var state_1 = tslib_1.__importDefault(require("app/components/forms/state"));
// TODO(dcramer): im not entirely sure this is working correctly with
// value propagation in all scenarios
var PasswordField = /** @class */ (function (_super) {
    tslib_1.__extends(PasswordField, _super);
    function PasswordField(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.cancelEdit = function (e) {
            e.preventDefault();
            _this.setState({
                editing: false,
            }, function () {
                _this.setValue('');
            });
        };
        _this.startEdit = function (e) {
            e.preventDefault();
            _this.setState({
                editing: true,
            });
        };
        _this.state = tslib_1.__assign(tslib_1.__assign({}, _this.state), { editing: false });
        return _this;
    }
    PasswordField.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // close edit mode after successful save
        // TODO(dcramer): this needs to work with this.context.form
        if (this.props.formState &&
            this.props.formState === state_1.default.SAVING &&
            nextProps.formState === state_1.default.READY) {
            this.setState({
                editing: false,
            });
        }
    };
    PasswordField.prototype.getType = function () {
        return 'password';
    };
    PasswordField.prototype.getField = function () {
        if (!this.props.hasSavedValue) {
            return _super.prototype.getField.call(this);
        }
        if (this.state.editing) {
            return (<div className="form-password editing">
          <div>{_super.prototype.getField.call(this)}</div>
          <div>
            <a onClick={this.cancelEdit}>Cancel</a>
          </div>
        </div>);
        }
        else {
            return (<div className="form-password saved">
          <span>
            {this.props.prefix + new Array(21 - this.props.prefix.length).join('*')}
          </span>
          {!this.props.disabled && <a onClick={this.startEdit}>Edit</a>}
        </div>);
        }
    };
    PasswordField.defaultProps = tslib_1.__assign(tslib_1.__assign({}, inputField_1.default.defaultProps), { hasSavedValue: false, prefix: '' });
    return PasswordField;
}(inputField_1.default));
exports.default = PasswordField;
//# sourceMappingURL=passwordField.jsx.map