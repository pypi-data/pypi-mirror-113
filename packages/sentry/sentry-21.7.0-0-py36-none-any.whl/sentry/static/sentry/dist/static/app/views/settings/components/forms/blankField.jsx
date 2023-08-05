Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
/**
 * This class is meant to hook into `fieldFromConfig`. Like the FieldSeparator
 * class, this doesn't have any fields of its own and is just meant to make
 * forms more flexible.
 */
var BlankField = /** @class */ (function (_super) {
    tslib_1.__extends(BlankField, _super);
    function BlankField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BlankField.prototype.render = function () {
        return <field_1.default {...this.props}/>;
    };
    return BlankField;
}(React.Component));
exports.default = BlankField;
//# sourceMappingURL=blankField.jsx.map