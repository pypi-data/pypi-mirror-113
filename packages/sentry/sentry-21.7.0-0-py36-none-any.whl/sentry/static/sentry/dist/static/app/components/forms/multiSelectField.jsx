Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var selectField_1 = tslib_1.__importDefault(require("app/components/forms/selectField"));
var MultiSelectField = /** @class */ (function (_super) {
    tslib_1.__extends(MultiSelectField, _super);
    function MultiSelectField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MultiSelectField.prototype.isMultiple = function () {
        return true;
    };
    return MultiSelectField;
}(selectField_1.default));
exports.default = MultiSelectField;
//# sourceMappingURL=multiSelectField.jsx.map