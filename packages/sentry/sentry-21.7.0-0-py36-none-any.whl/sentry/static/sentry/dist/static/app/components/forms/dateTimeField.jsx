Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var inputField_1 = tslib_1.__importDefault(require("app/components/forms/inputField"));
var DateTimeField = /** @class */ (function (_super) {
    tslib_1.__extends(DateTimeField, _super);
    function DateTimeField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DateTimeField.prototype.getType = function () {
        return 'datetime-local';
    };
    return DateTimeField;
}(inputField_1.default));
exports.default = DateTimeField;
//# sourceMappingURL=dateTimeField.jsx.map