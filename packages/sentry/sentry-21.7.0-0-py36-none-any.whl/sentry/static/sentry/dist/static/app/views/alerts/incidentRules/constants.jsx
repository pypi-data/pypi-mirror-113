var _a, _b;
Object.defineProperty(exports, "__esModule", { value: true });
exports.createRuleFromWizardTemplate = exports.createRuleFromEventView = exports.createDefaultRule = exports.createDefaultTrigger = exports.transactionFieldConfig = exports.wizardAlertFieldConfig = exports.getWizardAlertFieldConfig = exports.errorFieldConfig = exports.DATASOURCE_EVENT_TYPE_FILTERS = exports.DATASET_EVENT_TYPE_FILTERS = exports.DEFAULT_TRANSACTION_AGGREGATE = exports.DEFAULT_AGGREGATE = void 0;
var tslib_1 = require("tslib");
var constants_1 = require("app/utils/performance/vitals/constants");
var types_1 = require("app/views/alerts/incidentRules/types");
var utils_1 = require("app/views/alerts/utils");
exports.DEFAULT_AGGREGATE = 'count()';
exports.DEFAULT_TRANSACTION_AGGREGATE = 'p95(transaction.duration)';
exports.DATASET_EVENT_TYPE_FILTERS = (_a = {},
    _a[types_1.Dataset.ERRORS] = 'event.type:error',
    _a[types_1.Dataset.TRANSACTIONS] = 'event.type:transaction',
    _a);
exports.DATASOURCE_EVENT_TYPE_FILTERS = (_b = {},
    _b[types_1.Datasource.ERROR_DEFAULT] = '(event.type:error OR event.type:default)',
    _b[types_1.Datasource.ERROR] = 'event.type:error',
    _b[types_1.Datasource.DEFAULT] = 'event.type:default',
    _b[types_1.Datasource.TRANSACTION] = 'event.type:transaction',
    _b);
/**
 * Allowed error aggregations for alerts
 */
exports.errorFieldConfig = {
    aggregations: ['count', 'count_unique'],
    fields: ['user'],
};
var commonAggregations = [
    'avg',
    'percentile',
    'p50',
    'p75',
    'p95',
    'p99',
    'p100',
];
var allAggregations = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(commonAggregations)), [
    'failure_rate',
    'apdex',
    'count',
]);
function getWizardAlertFieldConfig(alertType, dataset) {
    if (alertType === 'custom' && dataset === types_1.Dataset.ERRORS) {
        return exports.errorFieldConfig;
    }
    // If user selected apdex we must include that in the OptionConfig as it has a user specified column
    var aggregations = alertType === 'apdex' || alertType === 'custom'
        ? allAggregations
        : commonAggregations;
    return {
        aggregations: aggregations,
        fields: ['transaction.duration'],
        measurementKeys: Object.keys(constants_1.WEB_VITAL_DETAILS),
    };
}
exports.getWizardAlertFieldConfig = getWizardAlertFieldConfig;
/**
 * Allowed aggregations for alerts created from wizard
 */
exports.wizardAlertFieldConfig = {
    aggregations: commonAggregations,
    fields: ['transaction.duration'],
    measurementKeys: Object.keys(constants_1.WEB_VITAL_DETAILS),
};
/**
 * Allowed transaction aggregations for alerts
 */
exports.transactionFieldConfig = {
    aggregations: allAggregations,
    fields: ['transaction.duration'],
    measurementKeys: Object.keys(constants_1.WEB_VITAL_DETAILS),
};
function createDefaultTrigger(label) {
    return {
        label: label,
        alertThreshold: '',
        actions: [],
    };
}
exports.createDefaultTrigger = createDefaultTrigger;
function createDefaultRule() {
    return {
        dataset: types_1.Dataset.ERRORS,
        eventTypes: [types_1.EventTypes.ERROR],
        aggregate: exports.DEFAULT_AGGREGATE,
        query: '',
        timeWindow: 1,
        triggers: [createDefaultTrigger('critical'), createDefaultTrigger('warning')],
        projects: [],
        environment: null,
        resolveThreshold: '',
        thresholdType: types_1.AlertRuleThresholdType.ABOVE,
    };
}
exports.createDefaultRule = createDefaultRule;
/**
 * Create an unsaved alert from a discover EventView object
 */
function createRuleFromEventView(eventView) {
    var _a;
    var parsedQuery = utils_1.getQueryDatasource(eventView.query);
    var datasetAndEventtypes = parsedQuery
        ? utils_1.DATA_SOURCE_TO_SET_AND_EVENT_TYPES[parsedQuery.source]
        : utils_1.DATA_SOURCE_TO_SET_AND_EVENT_TYPES.error;
    return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, createDefaultRule()), datasetAndEventtypes), { query: (_a = parsedQuery === null || parsedQuery === void 0 ? void 0 : parsedQuery.query) !== null && _a !== void 0 ? _a : eventView.query, 
        // If creating a metric alert for transactions, default to the p95 metric
        aggregate: datasetAndEventtypes.dataset === 'transactions'
            ? 'p95(transaction.duration)'
            : eventView.getYAxis(), environment: eventView.environment.length ? eventView.environment[0] : null });
}
exports.createRuleFromEventView = createRuleFromEventView;
function createRuleFromWizardTemplate(wizardTemplate) {
    var eventTypes = wizardTemplate.eventTypes, aggregateDataset = tslib_1.__rest(wizardTemplate, ["eventTypes"]);
    return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, createDefaultRule()), { eventTypes: [eventTypes] }), aggregateDataset);
}
exports.createRuleFromWizardTemplate = createRuleFromWizardTemplate;
//# sourceMappingURL=constants.jsx.map