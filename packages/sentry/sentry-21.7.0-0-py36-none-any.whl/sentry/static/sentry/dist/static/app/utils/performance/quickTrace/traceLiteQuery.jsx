Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function getTraceLiteRequestPayload(_a) {
    var eventId = _a.eventId, props = tslib_1.__rest(_a, ["eventId"]);
    var additionalApiPayload = utils_1.getTraceRequestPayload(props);
    return Object.assign({ event_id: eventId }, additionalApiPayload);
}
function EmptyTrace(_a) {
    var children = _a.children;
    return (<React.Fragment>
      {children({
            isLoading: false,
            error: null,
            trace: null,
            type: 'partial',
        })}
    </React.Fragment>);
}
function TraceLiteQuery(_a) {
    var traceId = _a.traceId, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, children = _a.children, props = tslib_1.__rest(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    var eventView = utils_1.makeEventView({ start: start, end: end, statsPeriod: statsPeriod });
    return (<genericDiscoverQuery_1.default route={"events-trace-light/" + traceId} getRequestPayload={getTraceLiteRequestPayload} beforeFetch={utils_1.beforeFetch} eventView={eventView} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return children(tslib_1.__assign({ 
                // This is using '||` instead of '??` here because
                // the client returns a empty string when the response
                // is 204. And we want the empty string, undefined and
                // null to be converted to null.
                trace: tableData || null, type: 'partial' }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = withApi_1.default(TraceLiteQuery);
//# sourceMappingURL=traceLiteQuery.jsx.map