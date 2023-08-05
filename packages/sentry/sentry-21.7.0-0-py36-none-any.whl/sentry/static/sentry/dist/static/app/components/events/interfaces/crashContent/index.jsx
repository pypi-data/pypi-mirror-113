Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var exception_1 = tslib_1.__importDefault(require("./exception"));
var stacktrace_1 = tslib_1.__importDefault(require("./stacktrace"));
var CrashContent = function (_a) {
    var _b;
    var event = _a.event, stackView = _a.stackView, stackType = _a.stackType, newestFirst = _a.newestFirst, projectId = _a.projectId, exception = _a.exception, stacktrace = _a.stacktrace;
    var platform = ((_b = event.platform) !== null && _b !== void 0 ? _b : 'other');
    if (exception) {
        return (<exception_1.default stackType={stackType} stackView={stackView} projectId={projectId} newestFirst={newestFirst} event={event} platform={platform} values={exception.values}/>);
    }
    if (stacktrace) {
        return (<stacktrace_1.default stacktrace={stacktrace} stackView={stackView} newestFirst={newestFirst} event={event} platform={platform}/>);
    }
    return null;
};
exports.default = CrashContent;
//# sourceMappingURL=index.jsx.map