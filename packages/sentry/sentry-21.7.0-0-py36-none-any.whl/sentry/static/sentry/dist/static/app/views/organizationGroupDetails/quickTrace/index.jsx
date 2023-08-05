Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var configureDistributedTracing_1 = tslib_1.__importDefault(require("./configureDistributedTracing"));
var issueQuickTrace_1 = tslib_1.__importDefault(require("./issueQuickTrace"));
function QuickTrace(_a) {
    var _b, _c;
    var event = _a.event, group = _a.group, organization = _a.organization, location = _a.location;
    var hasPerformanceView = organization.features.includes('performance-view');
    var hasTraceContext = Boolean((_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id);
    return (<react_1.Fragment>
      {!hasTraceContext && (<configureDistributedTracing_1.default event={event} project={group.project} organization={organization}/>)}
      {hasPerformanceView && hasTraceContext && (<issueQuickTrace_1.default organization={organization} event={event} location={location}/>)}
    </react_1.Fragment>);
}
exports.default = QuickTrace;
//# sourceMappingURL=index.jsx.map