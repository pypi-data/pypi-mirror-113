Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var EmailField = /** @class */ (function (_super) {
    tslib_1.__extends(EmailField, _super);
    function EmailField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EmailField.prototype.getType = function () {
        return 'email';
    };
    return EmailField;
}(inputField_1.default));
exports.default = EmailField;
//# sourceMappingURL=emailField.jsx.map