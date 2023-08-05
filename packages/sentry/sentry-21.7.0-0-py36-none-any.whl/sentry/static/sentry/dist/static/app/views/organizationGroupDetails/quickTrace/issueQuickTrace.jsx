Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var prompts_1 = require("app/actionCreators/prompts");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var quickTrace_1 = tslib_1.__importDefault(require("app/components/quickTrace"));
var utils_1 = require("app/components/quickTrace/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var quickTraceQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/quickTraceQuery"));
var promptIsDismissed_1 = require("app/utils/promptIsDismissed");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var IssueQuickTrace = /** @class */ (function (_super) {
    tslib_1.__extends(IssueQuickTrace, _super);
    function IssueQuickTrace() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: null,
        };
        _this.snoozePrompt = function () {
            var _a = _this.props, api = _a.api, event = _a.event, organization = _a.organization;
            var data = {
                projectId: event.projectID,
                organizationId: organization.id,
                feature: 'quick_trace_missing',
                status: 'snoozed',
            };
            prompts_1.promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        };
        return _this;
    }
    IssueQuickTrace.prototype.componentDidMount = function () {
        this.promptsCheck();
    };
    IssueQuickTrace.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event !== nextProps.event;
    };
    IssueQuickTrace.prototype.promptsCheck = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, event, organization, data;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, event = _a.event, organization = _a.organization;
                        return [4 /*yield*/, prompts_1.promptsCheck(api, {
                                organizationId: organization.id,
                                projectId: event.projectID,
                                feature: 'quick_trace_missing',
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: !promptIsDismissed_1.promptIsDismissed(data !== null && data !== void 0 ? data : {}, 30) });
                        return [2 /*return*/];
                }
            });
        });
    };
    IssueQuickTrace.prototype.handleTraceLink = function (organization) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'quick_trace.trace_id.clicked',
            eventName: 'Quick Trace: Trace ID clicked',
            organization_id: parseInt(organization.id, 10),
            source: 'issues',
        });
    };
    IssueQuickTrace.prototype.renderTraceLink = function (_a) {
        var _this = this;
        var isLoading = _a.isLoading, error = _a.error, trace = _a.trace, type = _a.type;
        var _b = this.props, event = _b.event, organization = _b.organization;
        if (isLoading || error !== null || trace === null || type === 'empty') {
            return null;
        }
        return (<LinkContainer>
        <react_router_1.Link to={utils_1.generateTraceTarget(event, organization)} onClick={function () { return _this.handleTraceLink(organization); }}>
          {locale_1.t('View Full Trace')}
        </react_router_1.Link>
      </LinkContainer>);
    };
    IssueQuickTrace.prototype.renderQuickTrace = function (results) {
        var _a = this.props, event = _a.event, location = _a.location, organization = _a.organization;
        var shouldShow = this.state.shouldShow;
        var isLoading = results.isLoading, error = results.error, trace = results.trace, type = results.type;
        if (isLoading) {
            return <placeholder_1.default height="24px"/>;
        }
        if (error || trace === null || trace.length === 0) {
            if (!shouldShow) {
                return null;
            }
            return (<StyledAlert type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <AlertContent>
            {locale_1.tct('The [type] for this error cannot be found. [link]', {
                    type: type === 'missing' ? locale_1.t('transaction') : locale_1.t('trace'),
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#troubleshooting">
                  {locale_1.t('Read the docs to understand why.')}
                </externalLink_1.default>),
                })}
            <button_1.default priority="link" title={locale_1.t('Dismiss for a month')} onClick={this.snoozePrompt}>
              <icons_1.IconClose />
            </button_1.default>
          </AlertContent>
        </StyledAlert>);
        }
        return (<quickTrace_1.default event={event} quickTrace={results} location={location} organization={organization} anchor="left" errorDest="issue" transactionDest="performance"/>);
    };
    IssueQuickTrace.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, organization = _a.organization, location = _a.location;
        return (<errorBoundary_1.default mini>
        <quickTraceQuery_1.default event={event} location={location} orgSlug={organization.slug}>
          {function (results) {
                return (<react_1.Fragment>
                {_this.renderTraceLink(results)}
                <QuickTraceWrapper>{_this.renderQuickTrace(results)}</QuickTraceWrapper>
              </react_1.Fragment>);
            }}
        </quickTraceQuery_1.default>
      </errorBoundary_1.default>);
    };
    return IssueQuickTrace;
}(react_1.Component));
var LinkContainer = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"], ["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"])), space_1.default(1), space_1.default(1), function (p) { return p.theme.border; });
var QuickTraceWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(0.5));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var AlertContent = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
exports.default = withApi_1.default(IssueQuickTrace);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=issueQuickTrace.jsx.map