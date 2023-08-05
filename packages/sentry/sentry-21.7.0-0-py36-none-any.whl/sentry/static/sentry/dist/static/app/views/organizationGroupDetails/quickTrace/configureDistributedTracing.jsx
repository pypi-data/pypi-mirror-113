Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var performance_quick_trace_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-quick-trace.svg"));
var prompts_1 = require("app/actionCreators/prompts");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var docs_1 = require("app/utils/docs");
var promptIsDismissed_1 = require("app/utils/promptIsDismissed");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var DISTRIBUTED_TRACING_FEATURE = 'distributed_tracing';
var ConfigureDistributedTracing = /** @class */ (function (_super) {
    tslib_1.__extends(ConfigureDistributedTracing, _super);
    function ConfigureDistributedTracing() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: null,
        };
        return _this;
    }
    ConfigureDistributedTracing.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ConfigureDistributedTracing.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, event, project, organization, data;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, event = _a.event, project = _a.project, organization = _a.organization;
                        if (!promptIsDismissed_1.promptCanShow(DISTRIBUTED_TRACING_FEATURE, event.eventID)) {
                            this.setState({ shouldShow: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, prompts_1.promptsCheck(api, {
                                projectId: project.id,
                                organizationId: organization.id,
                                feature: DISTRIBUTED_TRACING_FEATURE,
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: !promptIsDismissed_1.promptIsDismissed(data !== null && data !== void 0 ? data : {}, 30) });
                        return [2 /*return*/];
                }
            });
        });
    };
    ConfigureDistributedTracing.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, project = _b.project, organization = _b.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
            platform: project.platform,
        });
    };
    ConfigureDistributedTracing.prototype.handleClick = function (_a) {
        var _this = this;
        var action = _a.action, eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, api = _b.api, project = _b.project, organization = _b.organization;
        var data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: DISTRIBUTED_TRACING_FEATURE,
            status: action,
        };
        prompts_1.promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        this.trackAnalytics({ eventKey: eventKey, eventName: eventName });
    };
    ConfigureDistributedTracing.prototype.renderActionButton = function (docsLink) {
        var _this = this;
        var features = ['organizations:performance-view'];
        var noFeatureMessage = locale_1.t('Requires performance monitoring.');
        var renderDisabled = function (p) { return (<hovercard_1.default body={<featureDisabled_1.default features={features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
        {p.children(p)}
      </hovercard_1.default>); };
        return (<feature_1.default hookName="feature-disabled:configure-distributed-tracing" features={features} renderDisabled={renderDisabled}>
        {function () { return (<button_1.default size="small" priority="primary" href={docsLink} onClick={function () {
                    return _this.trackAnalytics({
                        eventKey: 'quick_trace.missing_instrumentation.docs',
                        eventName: 'Quick Trace: Missing Instrumentation Docs',
                    });
                }}>
            {locale_1.t('Read the docs')}
          </button_1.default>); }}
      </feature_1.default>);
    };
    ConfigureDistributedTracing.prototype.render = function () {
        var _this = this;
        var project = this.props.project;
        var shouldShow = this.state.shouldShow;
        if (!shouldShow) {
            return null;
        }
        var docsLink = docs_1.getConfigureTracingDocsLink(project);
        // if the platform does not support performance, do not show this prompt
        if (docsLink === null) {
            return null;
        }
        return (<ExampleQuickTracePanel dashedBorder>
        <div>
          <Header>{locale_1.t('Configure Distributed Tracing')}</Header>
          <Description>
            {locale_1.t('See what happened right before and after this error')}
          </Description>
        </div>
        <Image src={performance_quick_trace_svg_1.default} alt="configure distributed tracing"/>
        <ActionButtons>
          {this.renderActionButton(docsLink)}
          <buttonBar_1.default merged>
            <button_1.default title={locale_1.t('Remind me next month')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'snoozed',
                    eventKey: 'quick_trace.missing_instrumentation.snoozed',
                    eventName: 'Quick Trace: Missing Instrumentation Snoozed',
                });
            }}>
              {locale_1.t('Snooze')}
            </button_1.default>
            <button_1.default title={locale_1.t('Dismiss for this project')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'dismissed',
                    eventKey: 'quick_trace.missing_instrumentation.dismissed',
                    eventName: 'Quick Trace: Missing Instrumentation Dismissed',
                });
            }}>
              {locale_1.t('Dismiss')}
            </button_1.default>
          </buttonBar_1.default>
        </ActionButtons>
      </ExampleQuickTracePanel>);
    };
    return ConfigureDistributedTracing;
}(react_1.Component));
var ExampleQuickTracePanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1.5fr 1fr;\n  grid-template-rows: auto max-content;\n  grid-gap: ", ";\n  background: none;\n  padding: ", ";\n  margin: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: 1.5fr 1fr;\n  grid-template-rows: auto max-content;\n  grid-gap: ", ";\n  background: none;\n  padding: ", ";\n  margin: ", " 0;\n"])), space_1.default(1), space_1.default(2), space_1.default(2));
var Header = styled_1.default('h3')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space_1.default(1));
var Description = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var Image = styled_1.default('img')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-row: 1/3;\n  grid-column: 2/3;\n  justify-self: end;\n"], ["\n  grid-row: 1/3;\n  grid-column: 2/3;\n  justify-self: end;\n"])));
var ActionButtons = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content auto;\n  justify-items: start;\n  align-items: end;\n  grid-column-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content auto;\n  justify-items: start;\n  align-items: end;\n  grid-column-gap: ", ";\n"])), space_1.default(1));
exports.default = withApi_1.default(ConfigureDistributedTracing);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=configureDistributedTracing.jsx.map