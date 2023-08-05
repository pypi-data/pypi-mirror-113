Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
function PlatformHeaderButtonBar(_a) {
    var gettingStartedLink = _a.gettingStartedLink, docsLink = _a.docsLink;
    return (<buttonBar_1.default gap={1}>
      <button_1.default size="small" to={gettingStartedLink}>
        {locale_1.t('< Back')}
      </button_1.default>
      <button_1.default size="small" href={docsLink} external>
        {locale_1.t('Full Documentation')}
      </button_1.default>
    </buttonBar_1.default>);
}
exports.default = PlatformHeaderButtonBar;
//# sourceMappingURL=platformHeaderButtonBar.jsx.map