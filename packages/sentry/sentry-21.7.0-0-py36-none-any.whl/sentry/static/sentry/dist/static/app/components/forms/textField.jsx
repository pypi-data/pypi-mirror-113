Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var TextField = /** @class */ (function (_super) {
    tslib_1.__extends(TextField, _super);
    function TextField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TextField.prototype.getAttributes = function () {
        return {
            spellCheck: this.props.spellCheck,
        };
    };
    TextField.prototype.getType = function () {
        return 'text';
    };
    return TextField;
}(inputField_1.default));
exports.default = TextField;
//# sourceMappingURL=textField.jsx.map