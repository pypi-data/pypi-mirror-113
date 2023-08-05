Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var crashContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashContent"));
var crashActions_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashActions"));
var crashTitle_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashTitle"));
var stacktrace_1 = require("app/components/events/interfaces/stacktrace");
var locale_1 = require("app/locale");
var stacktrace_2 = require("app/types/stacktrace");
var defaultProps = {
    hideGuide: false,
};
var Exception = /** @class */ (function (_super) {
    tslib_1.__extends(Exception, _super);
    function Exception() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            stackView: _this.props.data.hasSystemFrames ? stacktrace_2.STACK_VIEW.APP : stacktrace_2.STACK_VIEW.FULL,
            newestFirst: stacktrace_1.isStacktraceNewestFirst(),
            stackType: stacktrace_2.STACK_TYPE.ORIGINAL,
        };
        _this.handleChange = function (newState) {
            _this.setState(function (prevState) { return (tslib_1.__assign(tslib_1.__assign({}, prevState), newState)); });
        };
        return _this;
    }
    Exception.prototype.render = function () {
        var eventHasThreads = !!this.props.event.entries.find(function (entry) { return entry.type === 'threads'; });
        // in case there are threads in the event data, we don't render the
        // exception block.  Instead the exception is contained within the
        // thread interface.
        if (eventHasThreads) {
            return null;
        }
        var _a = this.props, projectId = _a.projectId, event = _a.event, data = _a.data, hideGuide = _a.hideGuide, type = _a.type;
        var _b = this.state, stackView = _b.stackView, stackType = _b.stackType, newestFirst = _b.newestFirst;
        var commonCrashHeaderProps = {
            newestFirst: newestFirst,
            hideGuide: hideGuide,
            onChange: this.handleChange,
        };
        return (<eventDataSection_1.default type={type} title={<crashTitle_1.default title={locale_1.t('Exception')} {...commonCrashHeaderProps}/>} actions={<crashActions_1.default stackType={stackType} stackView={stackView} platform={event.platform} exception={data} {...commonCrashHeaderProps}/>} wrapTitle={false}>
        <crashContent_1.default projectId={projectId} event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} exception={data}/>
      </eventDataSection_1.default>);
    };
    Exception.defaultProps = {
        hideGuide: false,
    };
    return Exception;
}(react_1.Component));
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map