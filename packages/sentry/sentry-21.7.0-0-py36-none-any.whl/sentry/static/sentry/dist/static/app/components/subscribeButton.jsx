Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var SubscribeButton = /** @class */ (function (_super) {
    tslib_1.__extends(SubscribeButton, _super);
    function SubscribeButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SubscribeButton.prototype.render = function () {
        var _a = this.props, size = _a.size, isSubscribed = _a.isSubscribed, onClick = _a.onClick, disabled = _a.disabled;
        var icon = <icons_1.IconBell color={isSubscribed ? 'blue300' : undefined}/>;
        return (<button_1.default size={size} icon={icon} onClick={onClick} disabled={disabled}>
        {isSubscribed ? locale_1.t('Unsubscribe') : locale_1.t('Subscribe')}
      </button_1.default>);
    };
    return SubscribeButton;
}(React.Component));
exports.default = SubscribeButton;
//# sourceMappingURL=subscribeButton.jsx.map