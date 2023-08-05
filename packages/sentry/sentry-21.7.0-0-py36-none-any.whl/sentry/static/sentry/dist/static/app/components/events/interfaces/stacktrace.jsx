Object.defineProperty(exports, "__esModule", { value: true });
exports.isStacktraceNewestFirst = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var crashContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashContent"));
var crashActions_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashActions"));
var crashTitle_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashTitle"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var stacktrace_1 = require("app/types/stacktrace");
var noStackTraceMessage_1 = tslib_1.__importDefault(require("./noStackTraceMessage"));
function isStacktraceNewestFirst() {
    var user = configStore_1.default.get('user');
    // user may not be authenticated
    if (!user) {
        return true;
    }
    switch (user.options.stacktraceOrder) {
        case 2:
            return true;
        case 1:
            return false;
        case -1:
        default:
            return true;
    }
}
exports.isStacktraceNewestFirst = isStacktraceNewestFirst;
var defaultProps = {
    hideGuide: false,
};
var StacktraceInterface = /** @class */ (function (_super) {
    tslib_1.__extends(StacktraceInterface, _super);
    function StacktraceInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            stackView: _this.props.data.hasSystemFrames ? stacktrace_1.STACK_VIEW.APP : stacktrace_1.STACK_VIEW.FULL,
            newestFirst: isStacktraceNewestFirst(),
        };
        _this.handleChangeNewestFirst = function (_a) {
            var newestFirst = _a.newestFirst;
            _this.setState(function (prevState) { return (tslib_1.__assign(tslib_1.__assign({}, prevState), { newestFirst: newestFirst })); });
        };
        _this.handleChangeStackView = function (_a) {
            var stackView = _a.stackView;
            if (!stackView) {
                return;
            }
            _this.setState(function (prevState) { return (tslib_1.__assign(tslib_1.__assign({}, prevState), { stackView: stackView })); });
        };
        return _this;
    }
    StacktraceInterface.prototype.render = function () {
        var _a;
        var _b = this.props, projectId = _b.projectId, event = _b.event, data = _b.data, hideGuide = _b.hideGuide, type = _b.type;
        var _c = this.state, stackView = _c.stackView, newestFirst = _c.newestFirst;
        var stackTraceNotFound = !((_a = data.frames) !== null && _a !== void 0 ? _a : []).length;
        return (<eventDataSection_1.default type={type} title={<crashTitle_1.default title={locale_1.t('Stack Trace')} hideGuide={hideGuide} newestFirst={newestFirst} onChange={!stackTraceNotFound ? this.handleChangeNewestFirst : undefined}/>} actions={!stackTraceNotFound && (<crashActions_1.default stackView={stackView} platform={event.platform} stacktrace={data} onChange={this.handleChangeStackView}/>)} wrapTitle={false}>
        {stackTraceNotFound ? (<noStackTraceMessage_1.default />) : (<crashContent_1.default projectId={projectId} event={event} stackView={stackView} newestFirst={newestFirst} stacktrace={data} stackType={stacktrace_1.STACK_TYPE.ORIGINAL}/>)}
      </eventDataSection_1.default>);
    };
    StacktraceInterface.defaultProps = defaultProps;
    return StacktraceInterface;
}(React.Component));
exports.default = StacktraceInterface;
//# sourceMappingURL=stacktrace.jsx.map