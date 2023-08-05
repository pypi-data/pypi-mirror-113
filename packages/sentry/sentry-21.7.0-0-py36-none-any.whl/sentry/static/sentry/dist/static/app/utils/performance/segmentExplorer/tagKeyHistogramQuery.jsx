Object.defineProperty(exports, "__esModule", { value: true });
exports.getRequestFunction = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function getRequestFunction(_props) {
    var aggregateColumn = _props.aggregateColumn;
    function getTagExplorerRequestPayload(props) {
        var eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(props.location);
        apiPayload.aggregateColumn = aggregateColumn;
        apiPayload.sort = _props.sort ? _props.sort : '-sumdelta';
        apiPayload.tagKey = _props.tagKey;
        apiPayload.tagKeyLimit = _props.tagKeyLimit;
        apiPayload.numBucketsPerKey = _props.numBucketsPerKey;
        return apiPayload;
    }
    return getTagExplorerRequestPayload;
}
exports.getRequestFunction = getRequestFunction;
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.aggregateColumn !== nextProps.aggregateColumn ||
        prevProps.sort !== nextProps.sort ||
        prevProps.tagKey !== nextProps.tagKey);
}
function TagKeyHistogramQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-facets-performance-histogram" getRequestPayload={getRequestFunction(props)} shouldRefetchData={shouldRefetchData} {...props}/>);
}
exports.default = withApi_1.default(TagKeyHistogramQuery);
//# sourceMappingURL=tagKeyHistogramQuery.jsx.map