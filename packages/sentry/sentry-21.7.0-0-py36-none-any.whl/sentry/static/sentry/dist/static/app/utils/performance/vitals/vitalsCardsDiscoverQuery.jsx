Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var constants_1 = require("app/utils/performance/constants");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function getRequestPayload(props) {
    var eventView = props.eventView, vitals = props.vitals;
    var apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    return tslib_1.__assign({ vital: vitals }, pick_1.default(apiPayload, tslib_1.__spreadArray(['query'], tslib_1.__read(Object.values(constants_1.PERFORMANCE_URL_PARAM)))));
}
function VitalsCardsDiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default getRequestPayload={getRequestPayload} route="events-vitals" {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return props.children(tslib_1.__assign({ vitalsData: tableData }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = withApi_1.default(VitalsCardsDiscoverQuery);
//# sourceMappingURL=vitalsCardsDiscoverQuery.jsx.map