Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatar_1 = tslib_1.__importDefault(require("app/components/avatar"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/views/settings/account/notifications/utils");
/** TODO(mgaeta): Infer parentKey from parent. */
var ParentLabel = /** @class */ (function (_super) {
    tslib_1.__extends(ParentLabel, _super);
    function ParentLabel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.render = function () {
            var _a;
            var _b = _this.props, notificationType = _b.notificationType, parent = _b.parent;
            return (<FieldLabel>
        <avatar_1.default {..._a = {},
                _a[utils_1.getParentKey(notificationType)] = parent,
                _a}/>
        <span>{parent.slug}</span>
      </FieldLabel>);
        };
        return _this;
    }
    return ParentLabel;
}(react_1.default.Component));
var FieldLabel = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"], ["\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"])), space_1.default(0.5));
exports.default = ParentLabel;
var templateObject_1;
//# sourceMappingURL=parentLabel.jsx.map