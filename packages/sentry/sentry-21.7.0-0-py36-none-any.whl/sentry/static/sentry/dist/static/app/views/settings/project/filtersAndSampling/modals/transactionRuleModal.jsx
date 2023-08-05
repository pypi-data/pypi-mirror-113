Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var checkboxFancy_1 = tslib_1.__importDefault(require("app/components/checkboxFancy/checkboxFancy"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dynamicSampling_1 = require("app/types/dynamicSampling");
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var utils_1 = require("../utils");
var form_1 = tslib_1.__importDefault(require("./form"));
var utils_2 = require("./utils");
var TransactionRuleModal = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionRuleModal, _super);
    function TransactionRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteCondition = function (index) { return function () {
            var newConditions = tslib_1.__spreadArray([], tslib_1.__read(_this.state.conditions));
            newConditions.splice(index, 1);
            if (!newConditions.length) {
                _this.setState({
                    conditions: newConditions,
                    transaction: utils_2.Transaction.ALL,
                    isTracingDisabled: false,
                });
                return;
            }
            _this.setState({ conditions: newConditions });
        }; };
        _this.handleSubmit = function () {
            var _a = _this.state, tracing = _a.tracing, sampleRate = _a.sampleRate, conditions = _a.conditions, transaction = _a.transaction;
            if (!sampleRate) {
                return;
            }
            var _b = _this.props, rule = _b.rule, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            var newRule = {
                // All new/updated rules must have id equal to 0
                id: 0,
                type: tracing ? dynamicSampling_1.DynamicSamplingRuleType.TRACE : dynamicSampling_1.DynamicSamplingRuleType.TRANSACTION,
                condition: {
                    op: dynamicSampling_1.DynamicSamplingConditionOperator.AND,
                    inner: transaction === utils_2.Transaction.ALL ? [] : conditions.map(_this.getNewCondition),
                },
                sampleRate: sampleRate / 100,
            };
            var newTransactionRules = rule
                ? transactionRules.map(function (transactionRule) {
                    return isEqual_1.default(transactionRule, rule) ? newRule : transactionRule;
                })
                : tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(transactionRules)), [newRule]);
            var _c = tslib_1.__read(partition_1.default(newTransactionRules, function (transactionRule) { return transactionRule.type === dynamicSampling_1.DynamicSamplingRuleType.TRACE; }), 2), transactionTraceRules = _c[0], individualTransactionRules = _c[1];
            var newRules = tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(errorRules)), tslib_1.__read(transactionTraceRules)), tslib_1.__read(individualTransactionRules));
            var currentRuleIndex = newRules.findIndex(function (newR) { return newR === newRule; });
            _this.submitRules(newRules, currentRuleIndex);
        };
        return _this;
    }
    TransactionRuleModal.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevState.transaction !== this.state.transaction) {
            this.setIsTracingDisabled(this.state.transaction !== utils_2.Transaction.ALL);
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    TransactionRuleModal.prototype.setIsTracingDisabled = function (isTracingDisabled) {
        this.setState({ isTracingDisabled: isTracingDisabled });
    };
    TransactionRuleModal.prototype.getDefaultState = function () {
        var rule = this.props.rule;
        if (rule) {
            var condition = rule.condition;
            var inner = condition.inner;
            return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { tracing: rule.type === dynamicSampling_1.DynamicSamplingRuleType.TRACE, isTracingDisabled: !!inner.length });
        }
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { tracing: true });
    };
    TransactionRuleModal.prototype.getModalTitle = function () {
        var rule = this.props.rule;
        if (rule) {
            return locale_1.t('Edit Transaction Sampling Rule');
        }
        return locale_1.t('Add Transaction Sampling Rule');
    };
    TransactionRuleModal.prototype.geTransactionFieldDescription = function () {
        return {
            label: locale_1.t('Transactions'),
            help: locale_1.t('This determines if the rule applies to all transactions or only transactions that match custom conditions.'),
        };
    };
    TransactionRuleModal.prototype.getCategoryOptions = function () {
        var tracing = this.state.tracing;
        if (tracing) {
            return [
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE, locale_1.t('Releases')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT, locale_1.t('Environments')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID, locale_1.t('User Id')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_SEGMENT, locale_1.t('User Segment')],
            ];
        }
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
    TransactionRuleModal.prototype.getExtraFields = function () {
        var _this = this;
        var theme = this.props.theme;
        var _a = this.state, tracing = _a.tracing, isTracingDisabled = _a.isTracingDisabled;
        return (<field_1.default label={locale_1.t('Tracing')} 
        // help={t('this is a description')} // TODO(Priscila): Add correct descriptions
        inline={false} flexibleControlStateSize stacked showHelpInTooltip>
        <tooltip_1.default title={locale_1.t('This field can only be edited if there are no match conditions')} disabled={!isTracingDisabled} popperStyle={react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n            @media (min-width: ", ") {\n              max-width: 370px;\n            }\n          "], ["\n            @media (min-width: ", ") {\n              max-width: 370px;\n            }\n          "])), theme.breakpoints[0])}>
          <TracingWrapper onClick={isTracingDisabled ? undefined : function () { return _this.handleChange('tracing', !tracing); }}>
            <StyledCheckboxFancy isChecked={tracing} isDisabled={isTracingDisabled}/>
            {locale_1.tct('Include all related transactions by trace ID. This can span across multiple projects. All related errors will remain. [link:Learn more about tracing].', {
                link: (<externalLink_1.default href={utils_1.DYNAMIC_SAMPLING_DOC_LINK} onClick={function (event) { return event.stopPropagation(); }}/>),
            })}
          </TracingWrapper>
        </tooltip_1.default>
      </field_1.default>);
    };
    return TransactionRuleModal;
}(form_1.default));
exports.default = react_1.withTheme(TransactionRuleModal);
var TracingWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: ", ";\n"])), space_1.default(1), function (p) { return (p.onClick ? 'pointer' : 'not-allowed'); });
var StyledCheckboxFancy = styled_1.default(checkboxFancy_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionRuleModal.jsx.map