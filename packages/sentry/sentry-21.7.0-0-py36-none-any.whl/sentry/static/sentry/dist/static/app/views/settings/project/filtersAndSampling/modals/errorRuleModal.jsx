Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var locale_1 = require("app/locale");
var dynamicSampling_1 = require("app/types/dynamicSampling");
var form_1 = tslib_1.__importDefault(require("./form"));
var utils_1 = require("./utils");
var ErrorRuleModal = /** @class */ (function (_super) {
    tslib_1.__extends(ErrorRuleModal, _super);
    function ErrorRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function () {
            var _a = _this.state, sampleRate = _a.sampleRate, conditions = _a.conditions, transaction = _a.transaction;
            if (!sampleRate) {
                return;
            }
            var _b = _this.props, rule = _b.rule, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            var newRule = {
                // All new/updated rules must have id equal to 0
                id: 0,
                type: dynamicSampling_1.DynamicSamplingRuleType.ERROR,
                condition: {
                    op: dynamicSampling_1.DynamicSamplingConditionOperator.AND,
                    inner: transaction === utils_1.Transaction.ALL ? [] : conditions.map(_this.getNewCondition),
                },
                sampleRate: sampleRate / 100,
            };
            var newRules = rule
                ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(errorRules.map(function (errorRule) {
                    return isEqual_1.default(errorRule, rule) ? newRule : errorRule;
                }))), tslib_1.__read(transactionRules)) : tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(errorRules)), [newRule]), tslib_1.__read(transactionRules));
            var currentRuleIndex = newRules.findIndex(function (newR) { return newR === newRule; });
            _this.submitRules(newRules, currentRuleIndex);
        };
        return _this;
    }
    ErrorRuleModal.prototype.getDefaultState = function () {
        return tslib_1.__assign({}, _super.prototype.getDefaultState.call(this));
    };
    ErrorRuleModal.prototype.getModalTitle = function () {
        var rule = this.props.rule;
        if (rule) {
            return locale_1.t('Edit Error Sampling Rule');
        }
        return locale_1.t('Add Error Sampling Rule');
    };
    ErrorRuleModal.prototype.geTransactionFieldDescription = function () {
        return {
            label: locale_1.t('Errors'),
            help: locale_1.t('This determines if the rule applies to all errors or only errors that match custom conditions.'),
        };
    };
    ErrorRuleModal.prototype.getCategoryOptions = function () {
        return [
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE, locale_1.t('Releases')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT, locale_1.t('Environments')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID, locale_1.t('User Id')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT, locale_1.t('User Segment')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS, locale_1.t('Browser Extensions')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST, locale_1.t('Localhost')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER, locale_1.t('Legacy Browsers')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS, locale_1.t('Web Crawlers')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES, locale_1.t('IP Addresses')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP, locale_1.t('Content Security Policy')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES, locale_1.t('Error Messages')],
        ];
    };
    return ErrorRuleModal;
}(form_1.default));
exports.default = ErrorRuleModal;
//# sourceMappingURL=errorRuleModal.jsx.map