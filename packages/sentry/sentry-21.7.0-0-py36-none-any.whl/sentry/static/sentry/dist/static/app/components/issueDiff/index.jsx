Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueDiff = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getStacktraceBody_1 = tslib_1.__importDefault(require("app/utils/getStacktraceBody"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var renderGroupingInfo_1 = tslib_1.__importDefault(require("./renderGroupingInfo"));
var defaultProps = {
    baseEventId: 'latest',
    targetEventId: 'latest',
};
var IssueDiff = /** @class */ (function (_super) {
    tslib_1.__extends(IssueDiff, _super);
    function IssueDiff() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            groupingDiff: false,
            baseEvent: [],
            targetEvent: [],
            // `SplitDiffAsync` is an async-loaded component
            // This will eventually contain a reference to the exported component from `./splitDiff`
            SplitDiffAsync: undefined,
        };
        _this.toggleDiffMode = function () {
            _this.setState(function (state) { return ({ groupingDiff: !state.groupingDiff, loading: true }); }, _this.fetchData);
        };
        _this.fetchEventData = function (issueId, eventId) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, orgId, project, api, groupingDiff, paramEventId, event_1, groupingInfo, event;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, orgId = _a.orgId, project = _a.project, api = _a.api;
                        groupingDiff = this.state.groupingDiff;
                        paramEventId = eventId;
                        if (!(eventId === 'latest')) return [3 /*break*/, 2];
                        return [4 /*yield*/, api.requestPromise("/issues/" + issueId + "/events/latest/")];
                    case 1:
                        event_1 = _b.sent();
                        paramEventId = event_1.eventID;
                        _b.label = 2;
                    case 2:
                        if (!groupingDiff) return [3 /*break*/, 4];
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + project.slug + "/events/" + paramEventId + "/grouping-info/")];
                    case 3:
                        groupingInfo = _b.sent();
                        return [2 /*return*/, renderGroupingInfo_1.default(groupingInfo)];
                    case 4: return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + project.slug + "/events/" + paramEventId + "/")];
                    case 5:
                        event = _b.sent();
                        return [2 /*return*/, getStacktraceBody_1.default(event)];
                }
            });
        }); };
        return _this;
    }
    IssueDiff.prototype.componentDidMount = function () {
        this.fetchData();
    };
    IssueDiff.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, baseIssueId = _a.baseIssueId, targetIssueId = _a.targetIssueId, baseEventId = _a.baseEventId, targetEventId = _a.targetEventId;
        // Fetch component and event data
        Promise.all([
            Promise.resolve().then(function () { return tslib_1.__importStar(require('../splitDiff')); }),
            this.fetchEventData(baseIssueId, baseEventId !== null && baseEventId !== void 0 ? baseEventId : 'latest'),
            this.fetchEventData(targetIssueId, targetEventId !== null && targetEventId !== void 0 ? targetEventId : 'latest'),
        ])
            .then(function (_a) {
            var _b = tslib_1.__read(_a, 3), SplitDiffAsync = _b[0].default, baseEvent = _b[1], targetEvent = _b[2];
            _this.setState({
                SplitDiffAsync: SplitDiffAsync,
                baseEvent: baseEvent,
                targetEvent: targetEvent,
                loading: false,
            });
        })
            .catch(function () {
            indicator_1.addErrorMessage(locale_1.t('Error loading events'));
        });
    };
    IssueDiff.prototype.render = function () {
        var _a = this.props, className = _a.className, project = _a.project;
        var _b = this.state, DiffComponent = _b.SplitDiffAsync, loading = _b.loading, groupingDiff = _b.groupingDiff, baseEvent = _b.baseEvent, targetEvent = _b.targetEvent;
        var showDiffToggle = project.features.includes('similarity-view-v2');
        return (<StyledIssueDiff className={className} loading={loading}>
        {loading && <loadingIndicator_1.default />}
        {!loading && showDiffToggle && (<HeaderWrapper>
            <buttonBar_1.default merged active={groupingDiff ? 'grouping' : 'event'}>
              <button_1.default barId="event" size="small" onClick={this.toggleDiffMode}>
                {locale_1.t('Diff stack trace and message')}
              </button_1.default>
              <button_1.default barId="grouping" size="small" onClick={this.toggleDiffMode}>
                {locale_1.t('Diff grouping information')}
              </button_1.default>
            </buttonBar_1.default>
          </HeaderWrapper>)}
        {!loading &&
                DiffComponent &&
                baseEvent.map(function (value, i) {
                    var _a;
                    return (<DiffComponent key={i} base={value} target={(_a = targetEvent[i]) !== null && _a !== void 0 ? _a : ''} type="words"/>);
                })}
      </StyledIssueDiff>);
    };
    IssueDiff.defaultProps = defaultProps;
    return IssueDiff;
}(react_1.Component));
exports.IssueDiff = IssueDiff;
exports.default = withApi_1.default(IssueDiff);
var StyledIssueDiff = styled_1.default('div', {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'loading'; },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  overflow: auto;\n  padding: ", ";\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  ", ";\n"], ["\n  background-color: ", ";\n  overflow: auto;\n  padding: ", ";\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, space_1.default(1), function (p) {
    return p.loading &&
        "\n        background-color: " + p.theme.background + ";\n        justify-content: center;\n        align-items: center;\n      ";
});
var HeaderWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map