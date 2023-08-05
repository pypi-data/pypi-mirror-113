Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var TextareaField = /** @class */ (function (_super) {
    tslib_1.__extends(TextareaField, _super);
    function TextareaField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TextareaField.prototype.getField = function () {
        return (<textarea id={this.getId()} className="form-control" value={this.state.value} disabled={this.props.disabled} required={this.props.required} placeholder={this.props.placeholder} onChange={this.onChange.bind(this)}/>);
    };
    return TextareaField;
}(inputField_1.default));
exports.default = TextareaField;
//# sourceMappingURL=textareaField.jsx.map