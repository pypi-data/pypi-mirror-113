Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var SimplePasswordField = /** @class */ (function (_super) {
    tslib_1.__extends(SimplePasswordField, _super);
    function SimplePasswordField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SimplePasswordField.prototype.getType = function () {
        return 'password';
    };
    return SimplePasswordField;
}(inputField_1.default));
exports.default = SimplePasswordField;
//# sourceMappingURL=simplePasswordField.jsx.map