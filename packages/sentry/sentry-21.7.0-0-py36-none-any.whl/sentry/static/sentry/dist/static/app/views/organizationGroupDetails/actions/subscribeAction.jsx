Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("../utils");
function SubscribeAction(_a) {
    var _b, _c;
    var disabled = _a.disabled, group = _a.group, onClick = _a.onClick;
    var canChangeSubscriptionState = !((_c = (_b = group.subscriptionDetails) === null || _b === void 0 ? void 0 : _b.disabled) !== null && _c !== void 0 ? _c : false);
    if (!canChangeSubscriptionState) {
        return null;
    }
    return (<button_1.default disabled={disabled} title={utils_1.getSubscriptionReason(group, true)} priority={group.isSubscribed ? 'primary' : 'default'} size="zero" label={locale_1.t('Subscribe')} onClick={onClick} icon={<icons_1.IconBell size="xs"/>}/>);
}
exports.default = SubscribeAction;
//# sourceMappingURL=subscribeAction.jsx.map