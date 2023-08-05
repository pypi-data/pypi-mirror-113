Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getTraceKnownData_1 = tslib_1.__importDefault(require("./getTraceKnownData"));
var types_1 = require("./types");
var traceKnownDataValues = [
    types_1.TraceKnownDataType.STATUS,
    types_1.TraceKnownDataType.TRACE_ID,
    types_1.TraceKnownDataType.SPAN_ID,
    types_1.TraceKnownDataType.PARENT_SPAN_ID,
    types_1.TraceKnownDataType.TRANSACTION_NAME,
    types_1.TraceKnownDataType.OP_NAME,
];
var traceIgnoredDataValues = [];
var InnerTrace = withOrganization_1.default(function (_a) {
    var organization = _a.organization, event = _a.event, data = _a.data;
    return (<errorBoundary_1.default mini>
      <keyValueList_1.default data={getTraceKnownData_1.default(data, traceKnownDataValues, event, organization)} isSorted={false} raw={false}/>
      <keyValueList_1.default data={getUnknownData_1.default(data, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(traceKnownDataValues)), tslib_1.__read(traceIgnoredDataValues)))} isSorted={false} raw={false}/>
    </errorBoundary_1.default>);
});
var Trace = function (props) {
    return <InnerTrace {...props}/>;
};
exports.default = Trace;
//# sourceMappingURL=trace.jsx.map