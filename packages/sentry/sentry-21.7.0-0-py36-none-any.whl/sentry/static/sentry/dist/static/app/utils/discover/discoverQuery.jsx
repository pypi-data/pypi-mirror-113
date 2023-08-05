Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("./genericDiscoverQuery"));
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.transactionName !== nextProps.transactionName ||
        prevProps.transactionThreshold !== nextProps.transactionThreshold ||
        prevProps.transactionThresholdMetric !== nextProps.transactionThresholdMetric);
}
function DiscoverQuery(props) {
    return (<genericDiscoverQuery_1.default route="eventsv2" shouldRefetchData={shouldRefetchData} {...props}/>);
}
exports.default = withApi_1.default(DiscoverQuery);
//# sourceMappingURL=discoverQuery.jsx.map