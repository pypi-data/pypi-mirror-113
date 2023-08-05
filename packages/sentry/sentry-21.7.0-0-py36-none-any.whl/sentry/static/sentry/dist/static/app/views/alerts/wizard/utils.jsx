var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAlertTypeFromAggregateDataset = void 0;
var tslib_1 = require("tslib");
var types_1 = require("app/views/alerts/incidentRules/types");
// A set of unique identifiers to be able to tie aggregate and dataset back to a wizard alert type
var alertTypeIdentifiers = (_a = {},
    _a[types_1.Dataset.ERRORS] = {
        num_errors: 'count()',
        users_experiencing_errors: 'count_unique(tags[sentry:user])',
    },
    _a[types_1.Dataset.TRANSACTIONS] = {
        throughput: 'count()',
        trans_duration: 'transaction.duration',
        apdex: 'apdex',
        failure_rate: 'failure_rate()',
        lcp: 'measurements.lcp',
        fid: 'measurements.fid',
        cls: 'measurements.cls',
    },
    _a);
/**
 * Given an aggregate and dataset object, will return the corresponding wizard alert type
 * e.g. {aggregate: 'count()', dataset: 'events'} will yield 'num_errors'
 * @param template
 */
function getAlertTypeFromAggregateDataset(_a) {
    var aggregate = _a.aggregate, dataset = _a.dataset;
    var identifierForDataset = alertTypeIdentifiers[dataset];
    var matchingAlertTypeEntry = Object.entries(identifierForDataset).find(function (_a) {
        var _b = tslib_1.__read(_a, 2), _alertType = _b[0], identifier = _b[1];
        return identifier && aggregate.includes(identifier);
    });
    var alertType = matchingAlertTypeEntry && matchingAlertTypeEntry[0];
    return alertType ? alertType : 'custom';
}
exports.getAlertTypeFromAggregateDataset = getAlertTypeFromAggregateDataset;
//# sourceMappingURL=utils.jsx.map