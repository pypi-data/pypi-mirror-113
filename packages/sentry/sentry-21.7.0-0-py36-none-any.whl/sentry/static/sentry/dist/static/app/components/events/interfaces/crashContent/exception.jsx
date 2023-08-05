Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var exceptionContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/exceptionContent"));
var rawExceptionContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/rawExceptionContent"));
var stacktrace_1 = require("app/types/stacktrace");
var Exception = function (_a) {
    var stackView = _a.stackView, stackType = _a.stackType, projectId = _a.projectId, values = _a.values, event = _a.event, newestFirst = _a.newestFirst, _b = _a.platform, platform = _b === void 0 ? 'other' : _b;
    return (<errorBoundary_1.default mini>
    {stackView === stacktrace_1.STACK_VIEW.RAW ? (<rawExceptionContent_1.default eventId={event.id} projectId={projectId} type={stackType} values={values} platform={platform}/>) : (<exceptionContent_1.default type={stackType} stackView={stackView} values={values} platform={platform} newestFirst={newestFirst} event={event}/>)}
  </errorBoundary_1.default>);
};
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map