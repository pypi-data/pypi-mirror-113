Object.defineProperty(exports, "__esModule", { value: true });
exports.mapShowTransactionToPercentile = exports.filterEventsDisplayToLocationQuery = exports.decodeEventsDisplayFilterFromLocation = exports.eventsRouteWithQuery = exports.getEventsFilterOptions = exports.EventsDisplayFilterName = void 0;
var locale_1 = require("app/locale");
var queryString_1 = require("app/utils/queryString");
var filter_1 = require("../filter");
var utils_1 = require("../utils");
var EventsDisplayFilterName;
(function (EventsDisplayFilterName) {
    EventsDisplayFilterName["p50"] = "p50";
    EventsDisplayFilterName["p75"] = "p75";
    EventsDisplayFilterName["p95"] = "p95";
    EventsDisplayFilterName["p99"] = "p99";
    EventsDisplayFilterName["p100"] = "p100";
})(EventsDisplayFilterName = exports.EventsDisplayFilterName || (exports.EventsDisplayFilterName = {}));
function getEventsFilterOptions(spanOperationBreakdownFilter, percentileValues) {
    var _a;
    var _b = percentileValues
        ? percentileValues
        : { p99: 0, p95: 0, p75: 0, p50: 0 }, p99 = _b.p99, p95 = _b.p95, p75 = _b.p75, p50 = _b.p50;
    return _a = {},
        _a[EventsDisplayFilterName.p50] = {
            name: EventsDisplayFilterName.p50,
            query: p50 ? [['transaction.duration', "<=" + p50.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filter_1.filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: locale_1.t('p50'),
        },
        _a[EventsDisplayFilterName.p75] = {
            name: EventsDisplayFilterName.p75,
            query: p75 ? [['transaction.duration', "<=" + p75.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filter_1.filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: locale_1.t('p75'),
        },
        _a[EventsDisplayFilterName.p95] = {
            name: EventsDisplayFilterName.p95,
            query: p95 ? [['transaction.duration', "<=" + p95.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filter_1.filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: locale_1.t('p95'),
        },
        _a[EventsDisplayFilterName.p99] = {
            name: EventsDisplayFilterName.p99,
            query: p99 ? [['transaction.duration', "<=" + p99.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filter_1.filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: locale_1.t('p99'),
        },
        _a[EventsDisplayFilterName.p100] = {
            name: EventsDisplayFilterName.p100,
            label: locale_1.t('p100'),
        },
        _a;
}
exports.getEventsFilterOptions = getEventsFilterOptions;
function eventsRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query;
    var pathname = "/organizations/" + orgSlug + "/performance/summary/events/";
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
exports.eventsRouteWithQuery = eventsRouteWithQuery;
function stringToFilter(option) {
    if (Object.values(EventsDisplayFilterName).includes(option)) {
        return option;
    }
    return EventsDisplayFilterName.p100;
}
function decodeEventsDisplayFilterFromLocation(location) {
    return stringToFilter(queryString_1.decodeScalar(location.query.showTransactions, EventsDisplayFilterName.p100));
}
exports.decodeEventsDisplayFilterFromLocation = decodeEventsDisplayFilterFromLocation;
function filterEventsDisplayToLocationQuery(option, spanOperationBreakdownFilter) {
    var _a, _b;
    var eventsFilterOptions = getEventsFilterOptions(spanOperationBreakdownFilter);
    var kind = (_a = eventsFilterOptions[option].sort) === null || _a === void 0 ? void 0 : _a.kind;
    var field = (_b = eventsFilterOptions[option].sort) === null || _b === void 0 ? void 0 : _b.field;
    var query = {
        showTransactions: option,
    };
    if (kind && field) {
        query.sort = "" + (kind === 'desc' ? '-' : '') + field;
    }
    return query;
}
exports.filterEventsDisplayToLocationQuery = filterEventsDisplayToLocationQuery;
function mapShowTransactionToPercentile(showTransaction) {
    switch (showTransaction) {
        case utils_1.TransactionFilterOptions.OUTLIER:
            return EventsDisplayFilterName.p100;
        case utils_1.TransactionFilterOptions.SLOW:
            return EventsDisplayFilterName.p95;
        default:
            return undefined;
    }
}
exports.mapShowTransactionToPercentile = mapShowTransactionToPercentile;
//# sourceMappingURL=utils.jsx.map