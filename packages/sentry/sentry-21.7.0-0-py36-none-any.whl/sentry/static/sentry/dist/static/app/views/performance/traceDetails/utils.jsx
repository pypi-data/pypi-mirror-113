Object.defineProperty(exports, "__esModule", { value: true });
exports.isRootTransaction = exports.getTraceInfo = exports.getTraceDetailsUrl = void 0;
var tslib_1 = require("tslib");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var utils_1 = require("app/utils/performance/quickTrace/utils");
function getTraceDetailsUrl(organization, traceSlug, dateSelection, query) {
    var _a;
    var start = dateSelection.start, end = dateSelection.end, statsPeriod = dateSelection.statsPeriod;
    return {
        pathname: "/organizations/" + organization.slug + "/performance/trace/" + traceSlug + "/",
        query: tslib_1.__assign(tslib_1.__assign({}, query), (_a = { statsPeriod: statsPeriod }, _a[globalSelectionHeader_1.PAGE_URL_PARAM.PAGE_START] = start, _a[globalSelectionHeader_1.PAGE_URL_PARAM.PAGE_END] = end, _a)),
    };
}
exports.getTraceDetailsUrl = getTraceDetailsUrl;
function traceVisitor() {
    return function (accumulator, event) {
        var e_1, _a;
        var _b;
        try {
            for (var _c = tslib_1.__values((_b = event.errors) !== null && _b !== void 0 ? _b : []), _d = _c.next(); !_d.done; _d = _c.next()) {
                var error = _d.value;
                accumulator.errors.add(error.event_id);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_1) throw e_1.error; }
        }
        accumulator.transactions.add(event.event_id);
        accumulator.projects.add(event.project_slug);
        accumulator.startTimestamp = Math.min(accumulator.startTimestamp, event.start_timestamp);
        accumulator.endTimestamp = Math.max(accumulator.endTimestamp, event.timestamp);
        accumulator.maxGeneration = Math.max(accumulator.maxGeneration, event.generation);
        return accumulator;
    };
}
function getTraceInfo(traces) {
    var initial = {
        projects: new Set(),
        errors: new Set(),
        transactions: new Set(),
        startTimestamp: Number.MAX_SAFE_INTEGER,
        endTimestamp: 0,
        maxGeneration: 0,
    };
    return traces.reduce(function (info, trace) {
        return utils_1.reduceTrace(trace, traceVisitor(), info);
    }, initial);
}
exports.getTraceInfo = getTraceInfo;
function isRootTransaction(trace) {
    // Root transactions has no parent_span_id
    return trace.parent_span_id === null;
}
exports.isRootTransaction = isRootTransaction;
//# sourceMappingURL=utils.jsx.map