Object.defineProperty(exports, "__esModule", { value: true });
exports.STACKTRACE_PREVIEW_TOOLTIP_DELAY = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var stacktrace_1 = require("app/components/events/interfaces/stacktrace");
var stacktraceContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/stacktraceContent"));
var hovercard_1 = tslib_1.__importStar(require("app/components/hovercard"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var event_1 = require("app/types/event");
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var findBestThread_1 = tslib_1.__importDefault(require("./events/interfaces/threads/threadSelector/findBestThread"));
var getThreadStacktrace_1 = tslib_1.__importDefault(require("./events/interfaces/threads/threadSelector/getThreadStacktrace"));
var HOVERCARD_DELAY = 500;
exports.STACKTRACE_PREVIEW_TOOLTIP_DELAY = 1000;
var StacktracePreview = /** @class */ (function (_super) {
    tslib_1.__extends(StacktracePreview, _super);
    function StacktracePreview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            loadingVisible: false,
        };
        _this.loaderTimeout = null;
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, api, issueId, eventId, projectSlug, event_2, _b;
            var _this = this;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, api = _a.api, issueId = _a.issueId, eventId = _a.eventId, projectSlug = _a.projectSlug;
                        if (this.state.event || (!issueId && !(eventId && projectSlug))) {
                            return [2 /*return*/];
                        }
                        this.loaderTimeout = window.setTimeout(function () {
                            _this.setState({ loadingVisible: true });
                        }, HOVERCARD_DELAY);
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(eventId && projectSlug
                                ? "/projects/" + organization.slug + "/" + projectSlug + "/events/" + eventId + "/"
                                : "/issues/" + issueId + "/events/latest/")];
                    case 2:
                        event_2 = _c.sent();
                        clearTimeout(this.loaderTimeout);
                        this.setState({ event: event_2, loading: false, loadingVisible: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        clearTimeout(this.loaderTimeout);
                        this.setState({ loading: false, loadingVisible: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleStacktracePreviewClick = function (event) {
            event.stopPropagation();
        };
        return _this;
    }
    StacktracePreview.prototype.getStacktrace = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        var event = this.state.event;
        if (!event) {
            return undefined;
        }
        var exceptionsWithStacktrace = (_c = (_b = (_a = event.entries
            .find(function (e) { return e.type === event_1.EntryType.EXCEPTION; })) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.values.filter(function (_a) {
            var stacktrace = _a.stacktrace;
            return utils_1.defined(stacktrace);
        })) !== null && _c !== void 0 ? _c : [];
        var exceptionStacktrace = stacktrace_1.isStacktraceNewestFirst()
            ? (_d = exceptionsWithStacktrace[exceptionsWithStacktrace.length - 1]) === null || _d === void 0 ? void 0 : _d.stacktrace
            : (_e = exceptionsWithStacktrace[0]) === null || _e === void 0 ? void 0 : _e.stacktrace;
        if (exceptionStacktrace) {
            return exceptionStacktrace;
        }
        var threads = (_h = (_g = (_f = event.entries.find(function (e) { return e.type === event_1.EntryType.THREADS; })) === null || _f === void 0 ? void 0 : _f.data) === null || _g === void 0 ? void 0 : _g.values) !== null && _h !== void 0 ? _h : [];
        var bestThread = findBestThread_1.default(threads);
        if (!bestThread) {
            return undefined;
        }
        var bestThreadStacktrace = getThreadStacktrace_1.default(false, bestThread);
        if (bestThreadStacktrace) {
            return bestThreadStacktrace;
        }
        return undefined;
    };
    StacktracePreview.prototype.renderHovercardBody = function (stacktrace) {
        var _a, _b;
        var _c = this.state, event = _c.event, loading = _c.loading, loadingVisible = _c.loadingVisible;
        if (loading && loadingVisible) {
            return (<NoStackTraceWrapper>
          <loadingIndicator_1.default hideMessage size={32}/>
        </NoStackTraceWrapper>);
        }
        if (loading) {
            return null;
        }
        if (!stacktrace) {
            return (<NoStackTraceWrapper onClick={this.handleStacktracePreviewClick}>
          {locale_1.t("There's no stack trace available for this issue.")}
        </NoStackTraceWrapper>);
        }
        if (event) {
            return (<div onClick={this.handleStacktracePreviewClick}>
          <stacktraceContent_1.default data={stacktrace} expandFirstFrame={false} includeSystemFrames={((_a = stacktrace.frames) !== null && _a !== void 0 ? _a : []).every(function (frame) { return !frame.inApp; })} platform={((_b = event.platform) !== null && _b !== void 0 ? _b : 'other')} newestFirst={stacktrace_1.isStacktraceNewestFirst()} event={event} isHoverPreviewed/>
        </div>);
        }
        return null;
    };
    StacktracePreview.prototype.render = function () {
        var _a = this.props, children = _a.children, disablePreview = _a.disablePreview, theme = _a.theme, className = _a.className;
        var _b = this.state, loading = _b.loading, loadingVisible = _b.loadingVisible;
        var stacktrace = this.getStacktrace();
        if (disablePreview) {
            return children;
        }
        return (<span className={className} onMouseEnter={this.fetchData}>
        <StyledHovercard body={this.renderHovercardBody(stacktrace)} position="right" modifiers={{
                flip: {
                    enabled: false,
                },
                preventOverflow: {
                    padding: 20,
                    enabled: true,
                    boundariesElement: 'viewport',
                },
            }} state={loading && loadingVisible ? 'loading' : !stacktrace ? 'empty' : 'done'} tipBorderColor={theme.border} tipColor={theme.background}>
          {children}
        </StyledHovercard>
      </span>);
    };
    return StacktracePreview;
}(React.Component));
var StyledHovercard = styled_1.default(hovercard_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* Lower z-index to match the modals (10000 vs 10002) to allow stackTraceLinkModal be on top of stack trace preview. */\n  z-index: ", ";\n  width: ", ";\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow-y: auto;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  .loading {\n    margin: 0 auto;\n    .loading-indicator {\n      /**\n      * Overriding the .less file - for default 64px loader we have the width of border set to 6px\n      * For 32px we therefore need 3px to keep the same thickness ratio\n      */\n      border-width: 3px;\n    }\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  /* Lower z-index to match the modals (10000 vs 10002) to allow stackTraceLinkModal be on top of stack trace preview. */\n  z-index: ", ";\n  width: ", ";\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow-y: auto;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  .loading {\n    margin: 0 auto;\n    .loading-indicator {\n      /**\n      * Overriding the .less file - for default 64px loader we have the width of border set to 6px\n      * For 32px we therefore need 3px to keep the same thickness ratio\n      */\n      border-width: 3px;\n    }\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.zIndex.modal; }, function (p) {
    if (p.state === 'loading') {
        return 'auto';
    }
    if (p.state === 'empty') {
        return '340px';
    }
    return '700px';
}, hovercard_1.Body, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[2]; });
var NoStackTraceWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding: ", ";\n  font-size: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  min-height: 56px;\n"], ["\n  color: ", ";\n  padding: ", ";\n  font-size: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  min-height: 56px;\n"])), function (p) { return p.theme.subText; }, space_1.default(1.5), function (p) { return p.theme.fontSizeMedium; });
exports.default = withApi_1.default(react_1.withTheme(StacktracePreview));
var templateObject_1, templateObject_2;
//# sourceMappingURL=stacktracePreview.jsx.map