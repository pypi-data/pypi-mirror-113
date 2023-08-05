Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var rawStacktraceContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/rawStacktraceContent"));
var stacktraceContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/stacktraceContent"));
var stacktrace_1 = require("app/types/stacktrace");
var Stacktrace = function (_a) {
    var stackView = _a.stackView, stacktrace = _a.stacktrace, event = _a.event, newestFirst = _a.newestFirst, platform = _a.platform;
    return (<errorBoundary_1.default mini>
    {stackView === stacktrace_1.STACK_VIEW.RAW ? (<pre className="traceback plain">
        {rawStacktraceContent_1.default(stacktrace, event.platform)}
      </pre>) : (<stacktraceContent_1.default data={stacktrace} className="no-exception" includeSystemFrames={stackView === stacktrace_1.STACK_VIEW.FULL} platform={platform} event={event} newestFirst={newestFirst}/>)}
  </errorBoundary_1.default>);
};
exports.default = Stacktrace;
//# sourceMappingURL=stacktrace.jsx.map