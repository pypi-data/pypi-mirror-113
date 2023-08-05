Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var builderBreadCrumbs_1 = tslib_1.__importDefault(require("app/views/alerts/builder/builderBreadCrumbs"));
var details_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/details"));
var issueRuleEditor_1 = tslib_1.__importDefault(require("app/views/alerts/issueRuleEditor"));
var ProjectAlertsEditor = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectAlertsEditor, _super);
    function ProjectAlertsEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertType: '',
            ruleName: '',
        };
        _this.handleChangeTitle = function (ruleName) {
            _this.setState({ ruleName: ruleName });
        };
        return _this;
    }
    ProjectAlertsEditor.prototype.getTitle = function () {
        var ruleName = this.state.ruleName;
        return "" + ruleName;
    };
    ProjectAlertsEditor.prototype.render = function () {
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, location = _a.location, organization = _a.organization, project = _a.project, routes = _a.routes;
        var alertType = location.pathname.includes('/alerts/metric-rules/')
            ? 'metric'
            : 'issue';
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={this.getTitle()} orgSlug={organization.slug} projectSlug={project.slug}/>
        <Layout.Header>
          <Layout.HeaderContent>
            <builderBreadCrumbs_1.default hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} title={locale_1.t('Edit Alert Rule')} projectSlug={project.slug} routes={routes} location={location}/>
            <Layout.Title>{this.getTitle()}</Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <EditConditionsBody>
          <Layout.Main fullWidth>
            {(!hasMetricAlerts || alertType === 'issue') && (<issueRuleEditor_1.default {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
            {hasMetricAlerts && alertType === 'metric' && (<details_1.default {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
          </Layout.Main>
        </EditConditionsBody>
      </react_1.Fragment>);
    };
    return ProjectAlertsEditor;
}(react_1.Component));
var EditConditionsBody = styled_1.default(Layout.Body)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -", ";\n\n  *:not(img) {\n    max-width: 1000px;\n  }\n"], ["\n  margin-bottom: -", ";\n\n  *:not(img) {\n    max-width: 1000px;\n  }\n"])), space_1.default(3));
exports.default = ProjectAlertsEditor;
var templateObject_1;
//# sourceMappingURL=edit.jsx.map