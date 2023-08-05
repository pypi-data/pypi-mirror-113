Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var actionLink_1 = tslib_1.__importDefault(require("app/components/actions/actionLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
function ReviewAction(_a) {
    var disabled = _a.disabled, onUpdate = _a.onUpdate;
    return (<actionLink_1.default type="button" disabled={disabled} onAction={function () { return onUpdate({ inbox: false }); }} title={locale_1.t('Mark Reviewed')} icon={<icons_1.IconIssues size="xs"/>}>
      {locale_1.t('Mark Reviewed')}
    </actionLink_1.default>);
}
exports.default = ReviewAction;
//# sourceMappingURL=reviewAction.jsx.map