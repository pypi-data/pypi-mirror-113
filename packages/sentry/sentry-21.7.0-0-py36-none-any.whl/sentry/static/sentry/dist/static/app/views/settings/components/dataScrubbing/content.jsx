Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var rules_1 = tslib_1.__importDefault(require("./rules"));
var Content = function (_a) {
    var rules = _a.rules, disabled = _a.disabled, onDeleteRule = _a.onDeleteRule, onEditRule = _a.onEditRule;
    if (rules.length === 0) {
        return (<emptyMessage_1.default icon={<icons_1.IconWarning size="xl"/>} description={locale_1.t('You have no data scrubbing rules')}/>);
    }
    return (<rules_1.default rules={rules} onDeleteRule={onDeleteRule} onEditRule={onEditRule} disabled={disabled}/>);
};
exports.default = Content;
//# sourceMappingURL=content.jsx.map