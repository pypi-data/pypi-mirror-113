Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var locale_1 = require("app/locale");
var dynamicSampling_1 = require("app/types/dynamicSampling");
function Type(_a) {
    var type = _a.type;
    switch (type) {
        case dynamicSampling_1.DynamicSamplingRuleType.ERROR:
            return <ErrorLabel>{locale_1.t('Errors only')}</ErrorLabel>;
        case dynamicSampling_1.DynamicSamplingRuleType.TRANSACTION:
            return <TransactionLabel>{locale_1.t('Individual transactions')}</TransactionLabel>;
        case dynamicSampling_1.DynamicSamplingRuleType.TRACE:
            return <TransactionLabel>{locale_1.t('Transaction traces')}</TransactionLabel>;
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling rule type'));
            return null; // this shall never happen
        }
    }
}
exports.default = Type;
var ErrorLabel = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  white-space: pre-wrap;\n"], ["\n  color: ", ";\n  white-space: pre-wrap;\n"])), function (p) { return p.theme.pink300; });
var TransactionLabel = styled_1.default(ErrorLabel)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.linkColor; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=type.jsx.map