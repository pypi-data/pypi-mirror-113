Object.defineProperty(exports, "__esModule", { value: true });
exports.TrendsEventsDiscoverQuery = exports.getTrendsRequestPayload = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_1 = require("app/views/performance/trends/utils");
function getTrendsRequestPayload(props) {
    var eventView = props.eventView;
    var apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    var trendFunction = utils_1.getCurrentTrendFunction(props.location);
    var trendParameter = utils_1.getCurrentTrendParameter(props.location);
    apiPayload.trendFunction = utils_1.generateTrendFunctionAsString(trendFunction.field, trendParameter.column);
    apiPayload.trendType = eventView === null || eventView === void 0 ? void 0 : eventView.trendType;
    apiPayload.interval = eventView === null || eventView === void 0 ? void 0 : eventView.interval;
    apiPayload.middle = eventView === null || eventView === void 0 ? void 0 : eventView.middle;
    return apiPayload;
}
exports.getTrendsRequestPayload = getTrendsRequestPayload;
function TrendsDiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-trends-stats" getRequestPayload={getTrendsRequestPayload} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return props.children(tslib_1.__assign({ trendsData: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
function EventsDiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-trends" getRequestPayload={getTrendsRequestPayload} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return props.children(tslib_1.__assign({ trendsData: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.TrendsEventsDiscoverQuery = withApi_1.default(EventsDiscoverQuery);
exports.default = withApi_1.default(TrendsDiscoverQuery);
//# sourceMappingURL=trendsDiscoverQuery.jsx.map