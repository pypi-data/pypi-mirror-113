Object.defineProperty(exports, "__esModule", { value: true });
exports.TraceFullDetailedQuery = exports.TraceFullQuery = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function getTraceFullRequestPayload(_a) {
    var detailed = _a.detailed, eventId = _a.eventId, props = tslib_1.__rest(_a, ["detailed", "eventId"]);
    var additionalApiPayload = utils_1.getTraceRequestPayload(props);
    additionalApiPayload.detailed = detailed ? '1' : '0';
    if (eventId) {
        additionalApiPayload.event_id = eventId;
    }
    return additionalApiPayload;
}
function EmptyTrace(_a) {
    var children = _a.children;
    return (<React.Fragment>
      {children({
            isLoading: false,
            error: null,
            traces: null,
            type: 'full',
        })}
    </React.Fragment>);
}
function GenericTraceFullQuery(_a) {
    var traceId = _a.traceId, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, children = _a.children, props = tslib_1.__rest(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    var eventView = utils_1.makeEventView({ start: start, end: end, statsPeriod: statsPeriod });
    return (<genericDiscoverQuery_1.default route={"events-trace/" + traceId} getRequestPayload={getTraceFullRequestPayload} beforeFetch={utils_1.beforeFetch} eventView={eventView} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return children(tslib_1.__assign({ 
                // This is using '||` instead of '??` here because
                // the client returns a empty string when the response
                // is 204. And we want the empty string, undefined and
                // null to be converted to null.
                traces: tableData || null, type: 'full' }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.TraceFullQuery = withApi_1.default(function (props) { return (<GenericTraceFullQuery {...props} detailed={false}/>); });
exports.TraceFullDetailedQuery = withApi_1.default(function (props) { return (<GenericTraceFullQuery {...props} detailed/>); });
//# sourceMappingURL=traceFullQuery.jsx.map