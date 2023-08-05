Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var commandLine_1 = tslib_1.__importDefault(require("app/components/commandLine"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var WaitingActivity = function (_a) {
    var onRefresh = _a.onRefresh, disabled = _a.disabled;
    return (<panels_1.Panel>
    <emptyMessage_1.default title={locale_1.t('Waiting on Activity!')} description={disabled
            ? undefined
            : locale_1.tct('Run relay in your terminal with [commandLine]', {
                commandLine: <commandLine_1.default>{'relay run'}</commandLine_1.default>,
            })} action={<button_1.default icon={<icons_1.IconRefresh />} onClick={onRefresh}>
          {locale_1.t('Refresh')}
        </button_1.default>}/>
  </panels_1.Panel>);
};
exports.default = WaitingActivity;
//# sourceMappingURL=waitingActivity.jsx.map