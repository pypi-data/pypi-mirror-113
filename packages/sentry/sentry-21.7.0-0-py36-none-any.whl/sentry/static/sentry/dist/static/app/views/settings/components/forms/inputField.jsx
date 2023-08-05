Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var InputField = /** @class */ (function (_super) {
    tslib_1.__extends(InputField, _super);
    function InputField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputField.prototype.render = function () {
        var _a = this.props, className = _a.className, field = _a.field;
        return (<formField_1.default className={className} {...this.props}>
        {function (formFieldProps) { return field && field(omit_1.default(formFieldProps, 'children')); }}
      </formField_1.default>);
    };
    InputField.defaultProps = {
        field: function (_a) {
            var onChange = _a.onChange, onBlur = _a.onBlur, onKeyDown = _a.onKeyDown, props = tslib_1.__rest(_a, ["onChange", "onBlur", "onKeyDown"]);
            return (<input_1.default {...props} onBlur={function (e) { return onBlur(e.target.value, e); }} onKeyDown={function (e) { return onKeyDown(e.target.value, e); }} onChange={function (e) { return onChange(e.target.value, e); }}/>);
        },
    };
    return InputField;
}(React.Component));
exports.default = InputField;
//# sourceMappingURL=inputField.jsx.map