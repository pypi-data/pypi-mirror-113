Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var ProjectPerformance = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectPerformance, _super);
    function ProjectPerformance() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            var organization = _this.props.organization;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/transaction-threshold/configure/", {
                method: 'DELETE',
                success: function () {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'performance_views.project_transaction_threshold.clear',
                        eventName: 'Project Transaction Threshold: Cleared',
                        organization_id: organization.id,
                    });
                },
                complete: function () { return _this.fetchData(); },
            });
        };
        return _this;
    }
    ProjectPerformance.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Performance'), projectId, false);
    };
    ProjectPerformance.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            ['threshold', "/projects/" + orgId + "/" + projectId + "/transaction-threshold/configure/"],
        ];
        return endpoints;
    };
    ProjectPerformance.prototype.getEmptyMessage = function () {
        return locale_1.t('There is no threshold set for this project.');
    };
    ProjectPerformance.prototype.renderLoading = function () {
        return (<LoadingIndicatorContainer>
        <loadingIndicator_1.default />
      </LoadingIndicatorContainer>);
    };
    Object.defineProperty(ProjectPerformance.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'metric',
                    type: 'select',
                    label: locale_1.t('Calculation Method'),
                    choices: [
                        ['duration', locale_1.t('Transaction Duration')],
                        ['lcp', locale_1.t('Largest Contentful Paint')],
                    ],
                    help: locale_1.tct('This determines which duration is used to set your thresholds. By default, we use transaction duration which measures the entire length of the transaction. You can also set this to use a [link:Web Vital].', {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/performance/web-vitals/"/>),
                    }),
                },
                {
                    name: 'threshold',
                    type: 'string',
                    label: locale_1.t('Response Time Threshold (ms)'),
                    placeholder: locale_1.t('300'),
                    help: locale_1.tct('Define what a satisfactory response time is based on the calculation method above. This will affect how your [link1:Apdex] and [link2:User Misery] thresholds are calculated. For example, misery will be 4x your satisfactory response time.', {
                        link1: (<externalLink_1.default href="https://docs.sentry.io/performance-monitoring/performance/metrics/#apdex"/>),
                        link2: (<externalLink_1.default href="https://docs.sentry.io/product/performance/metrics/#user-misery"/>),
                    }),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectPerformance.prototype, "initialData", {
        get: function () {
            var threshold = this.state.threshold;
            return {
                threshold: threshold.threshold,
                metric: threshold.metric,
            };
        },
        enumerable: false,
        configurable: true
    });
    ProjectPerformance.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, project = _a.project;
        var endpoint = "/projects/" + organization.slug + "/" + project.slug + "/transaction-threshold/configure/";
        return (<react_1.default.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Performance')}/>
        <permissionAlert_1.default />
        <form_1.default saveOnBlur allowUndo initialData={this.initialData} apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={function (resp) {
                var initial = _this.initialData;
                var changedThreshold = initial.metric === resp.metric;
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'performance_views.project_transaction_threshold.change',
                    eventName: 'Project Transaction Threshold: Changed',
                    organization_id: organization.id,
                    from: changedThreshold ? initial.threshold : initial.metric,
                    to: changedThreshold ? resp.threshold : resp.metric,
                    key: changedThreshold ? 'threshold' : 'metric',
                });
                _this.setState({ threshold: resp });
            }}>
          <jsonForm_1.default title={locale_1.t('General')} fields={this.formFields} renderFooter={function () { return (<Actions>
                <button_1.default onClick={function () { return _this.handleDelete(); }}>{locale_1.t('Reset All')}</button_1.default>
              </Actions>); }}/>
        </form_1.default>
      </react_1.default.Fragment>);
    };
    return ProjectPerformance;
}(asyncView_1.default));
var Actions = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var LoadingIndicatorContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 18px 18px 0;\n"], ["\n  margin: 18px 18px 0;\n"])));
exports.default = ProjectPerformance;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectPerformance.jsx.map