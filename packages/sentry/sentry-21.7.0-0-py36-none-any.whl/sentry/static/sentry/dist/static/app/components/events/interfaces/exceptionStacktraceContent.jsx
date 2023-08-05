Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var stacktraceContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/stacktraceContent"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var stacktrace_1 = require("app/types/stacktrace");
var utils_1 = require("app/utils");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var ExceptionStacktraceContent = function (_a) {
    var _b, _c;
    var stackView = _a.stackView, stacktrace = _a.stacktrace, chainedException = _a.chainedException, platform = _a.platform, newestFirst = _a.newestFirst, data = _a.data, expandFirstFrame = _a.expandFirstFrame, event = _a.event;
    if (!utils_1.defined(stacktrace)) {
        return null;
    }
    if (stackView === stacktrace_1.STACK_VIEW.APP &&
        ((_b = stacktrace.frames) !== null && _b !== void 0 ? _b : []).filter(function (frame) { return frame.inApp; }).length === 0 &&
        !chainedException) {
        return (<panels_1.Panel dashedBorder>
        <emptyMessage_1.default icon={<icons_1.IconWarning size="xs"/>} title={locale_1.t('No app only stack trace has been found!')}/>
      </panels_1.Panel>);
    }
    if (!data) {
        return null;
    }
    /**
     * Armin, Markus:
     * If all frames are in app, then no frame is in app.
     * This normally does not matter for the UI but when chained exceptions
     * are used this causes weird behavior where one exception appears to not have a stack trace.
     *
     * It is easier to fix the UI logic to show a non-empty stack trace for chained exceptions
     */
    return (<stacktraceContent_1.default data={data} expandFirstFrame={expandFirstFrame} includeSystemFrames={stackView === stacktrace_1.STACK_VIEW.FULL ||
            (chainedException && ((_c = stacktrace.frames) !== null && _c !== void 0 ? _c : []).every(function (frame) { return !frame.inApp; }))} platform={platform} newestFirst={newestFirst} event={event}/>);
};
exports.default = ExceptionStacktraceContent;
//# sourceMappingURL=exceptionStacktraceContent.jsx.map