Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var crashActions_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashActions"));
var crashTitle_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashTitle"));
var stacktrace_1 = require("app/components/events/interfaces/stacktrace");
var locale_1 = require("app/locale");
var stacktrace_2 = require("app/types/stacktrace");
var utils_1 = require("app/utils");
var findBestThread_1 = tslib_1.__importDefault(require("./threadSelector/findBestThread"));
var getThreadException_1 = tslib_1.__importDefault(require("./threadSelector/getThreadException"));
var getThreadStacktrace_1 = tslib_1.__importDefault(require("./threadSelector/getThreadStacktrace"));
var content_1 = tslib_1.__importDefault(require("./content"));
var threadSelector_1 = tslib_1.__importDefault(require("./threadSelector"));
var defaultProps = {
    hideGuide: false,
};
function getIntendedStackView(thread, event) {
    var exception = getThreadException_1.default(event, thread);
    if (exception) {
        return !!exception.values.find(function (value) { var _a; return !!((_a = value.stacktrace) === null || _a === void 0 ? void 0 : _a.hasSystemFrames); })
            ? stacktrace_2.STACK_VIEW.APP
            : stacktrace_2.STACK_VIEW.FULL;
    }
    var stacktrace = getThreadStacktrace_1.default(false, thread);
    return (stacktrace === null || stacktrace === void 0 ? void 0 : stacktrace.hasSystemFrames) ? stacktrace_2.STACK_VIEW.APP : stacktrace_2.STACK_VIEW.FULL;
}
var Threads = /** @class */ (function (_super) {
    tslib_1.__extends(Threads, _super);
    function Threads() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleSelectNewThread = function (thread) {
            _this.setState(function (prevState) { return ({
                activeThread: thread,
                stackView: prevState.stackView !== stacktrace_2.STACK_VIEW.RAW
                    ? getIntendedStackView(thread, _this.props.event)
                    : prevState.stackView,
                stackType: stacktrace_2.STACK_TYPE.ORIGINAL,
            }); });
        };
        _this.handleChangeNewestFirst = function (_a) {
            var newestFirst = _a.newestFirst;
            _this.setState({ newestFirst: newestFirst });
        };
        _this.handleChangeStackView = function (_a) {
            var stackView = _a.stackView, stackType = _a.stackType;
            _this.setState(function (prevState) { return ({
                stackView: stackView !== null && stackView !== void 0 ? stackView : prevState.stackView,
                stackType: stackType !== null && stackType !== void 0 ? stackType : prevState.stackType,
            }); });
        };
        return _this;
    }
    Threads.prototype.getInitialState = function () {
        var _a = this.props, data = _a.data, event = _a.event;
        var thread = utils_1.defined(data.values) ? findBestThread_1.default(data.values) : undefined;
        return {
            activeThread: thread,
            stackView: thread ? getIntendedStackView(thread, event) : undefined,
            stackType: stacktrace_2.STACK_TYPE.ORIGINAL,
            newestFirst: stacktrace_1.isStacktraceNewestFirst(),
        };
    };
    Threads.prototype.render = function () {
        var _a = this.props, data = _a.data, event = _a.event, projectId = _a.projectId, hideGuide = _a.hideGuide, type = _a.type;
        if (!data.values) {
            return null;
        }
        var threads = data.values;
        var _b = this.state, stackView = _b.stackView, stackType = _b.stackType, newestFirst = _b.newestFirst, activeThread = _b.activeThread;
        var exception = getThreadException_1.default(event, activeThread);
        var stacktrace = !exception
            ? getThreadStacktrace_1.default(stackType !== stacktrace_2.STACK_TYPE.ORIGINAL, activeThread)
            : undefined;
        var stackTraceNotFound = !(exception || stacktrace);
        var hasMoreThanOneThread = threads.length > 1;
        return (<eventDataSection_1.default type={type} title={hasMoreThanOneThread ? (<crashTitle_1.default title="" newestFirst={newestFirst} hideGuide={hideGuide} onChange={this.handleChangeNewestFirst} beforeTitle={activeThread && (<threadSelector_1.default threads={threads} activeThread={activeThread} event={event} onChange={this.handleSelectNewThread} exception={exception}/>)}/>) : (<crashTitle_1.default title={locale_1.t('Stack Trace')} newestFirst={newestFirst} hideGuide={hideGuide} onChange={!stackTraceNotFound ? this.handleChangeNewestFirst : undefined}/>)} actions={!stackTraceNotFound && (<crashActions_1.default stackView={stackView} platform={event.platform} stacktrace={stacktrace} stackType={stackType} thread={hasMoreThanOneThread ? activeThread : undefined} exception={exception} onChange={this.handleChangeStackView}/>)} showPermalink={!hasMoreThanOneThread} wrapTitle={false}>
        <content_1.default data={activeThread} exception={exception} stackView={stackView} stackType={stackType} stacktrace={stacktrace} event={event} newestFirst={newestFirst} projectId={projectId} stackTraceNotFound={stackTraceNotFound}/>
      </eventDataSection_1.default>);
    };
    Threads.defaultProps = defaultProps;
    return Threads;
}(react_1.Component));
exports.default = Threads;
//# sourceMappingURL=index.jsx.map