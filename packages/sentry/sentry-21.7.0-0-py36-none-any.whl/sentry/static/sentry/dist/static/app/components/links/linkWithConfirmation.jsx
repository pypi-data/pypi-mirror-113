Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
/**
 * <Confirm> is a more generic version of this component
 */
var LinkWithConfirmation = /** @class */ (function (_super) {
    tslib_1.__extends(LinkWithConfirmation, _super);
    function LinkWithConfirmation() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LinkWithConfirmation.prototype.render = function () {
        var _a = this.props, className = _a.className, disabled = _a.disabled, title = _a.title, children = _a.children, otherProps = tslib_1.__rest(_a, ["className", "disabled", "title", "children"]);
        return (<confirm_1.default {...otherProps} disabled={disabled}>
        <a href="#" className={classnames_1.default(className || '', { disabled: disabled })} title={title}>
          {children}
        </a>
      </confirm_1.default>);
    };
    return LinkWithConfirmation;
}(React.PureComponent));
exports.default = LinkWithConfirmation;
//# sourceMappingURL=linkWithConfirmation.jsx.map