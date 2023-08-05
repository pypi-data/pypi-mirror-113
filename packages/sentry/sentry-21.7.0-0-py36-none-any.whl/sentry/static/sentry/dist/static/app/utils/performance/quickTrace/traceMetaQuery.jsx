Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function TraceMetaQuery(_a) {
    var traceId = _a.traceId, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, children = _a.children, props = tslib_1.__rest(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                meta: null,
            })}
      </React.Fragment>);
    }
    var eventView = utils_1.makeEventView({ start: start, end: end, statsPeriod: statsPeriod });
    return (<genericDiscoverQuery_1.default route={"events-trace-meta/" + traceId} beforeFetch={utils_1.beforeFetch} getRequestPayload={utils_1.getTraceRequestPayload} eventView={eventView} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return children(tslib_1.__assign({ meta: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = withApi_1.default(TraceMetaQuery);
//# sourceMappingURL=traceMetaQuery.jsx.map