Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var utils_1 = require("app/components/events/interfaces/frame/utils");
var getRelevantFrame_1 = tslib_1.__importDefault(require("./getRelevantFrame"));
var getThreadException_1 = tslib_1.__importDefault(require("./getThreadException"));
var getThreadStacktrace_1 = tslib_1.__importDefault(require("./getThreadStacktrace"));
var trimFilename_1 = tslib_1.__importDefault(require("./trimFilename"));
function filterThreadInfo(event, thread, exception) {
    var _a;
    var threadInfo = {};
    var stacktrace = getThreadStacktrace_1.default(false, thread);
    if (thread.crashed) {
        var threadException = exception !== null && exception !== void 0 ? exception : getThreadException_1.default(event, thread);
        var matchedStacktraceAndExceptionThread = threadException === null || threadException === void 0 ? void 0 : threadException.values.find(function (exceptionDataValue) { return exceptionDataValue.threadId === thread.id; });
        if (matchedStacktraceAndExceptionThread) {
            stacktrace = (_a = matchedStacktraceAndExceptionThread.stacktrace) !== null && _a !== void 0 ? _a : undefined;
        }
        threadInfo.crashedInfo = threadException;
    }
    if (!stacktrace) {
        return threadInfo;
    }
    var relevantFrame = getRelevantFrame_1.default(stacktrace);
    if (relevantFrame.filename) {
        threadInfo.filename = trimFilename_1.default(relevantFrame.filename);
    }
    if (relevantFrame.function) {
        threadInfo.label = relevantFrame.function;
        return threadInfo;
    }
    if (relevantFrame.package) {
        threadInfo.label = utils_1.trimPackage(relevantFrame.package);
        return threadInfo;
    }
    if (relevantFrame.module) {
        threadInfo.label = relevantFrame.module;
        return threadInfo;
    }
    return threadInfo;
}
exports.default = filterThreadInfo;
//# sourceMappingURL=filterThreadInfo.jsx.map