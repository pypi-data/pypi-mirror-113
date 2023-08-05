Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var projectIssueGrouping_1 = require("app/data/forms/projectIssueGrouping");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var upgradeGrouping_1 = tslib_1.__importDefault(require("./upgradeGrouping"));
var ProjectDebugSymbols = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectDebugSymbols, _super);
    function ProjectDebugSymbols() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (response) {
            // This will update our project context
            projectActions_1.default.updateSuccess(response);
        };
        return _this;
    }
    ProjectDebugSymbols.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Issue Grouping'), projectId, false);
    };
    ProjectDebugSymbols.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { groupingConfigs: [] });
    };
    ProjectDebugSymbols.prototype.getEndpoints = function () {
        return [['groupingConfigs', '/grouping-configs/']];
    };
    ProjectDebugSymbols.prototype.renderBody = function () {
        var groupingConfigs = this.state.groupingConfigs;
        var _a = this.props, organization = _a.organization, project = _a.project, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoint = "/projects/" + orgId + "/" + projectId + "/";
        var access = new Set(organization.access);
        var jsonFormProps = {
            additionalFieldProps: {
                organization: organization,
                groupingConfigs: groupingConfigs,
            },
            features: new Set(organization.features),
            access: access,
            disabled: !access.has('project:write'),
        };
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Issue Grouping')}/>

        <textBlock_1.default>
          {locale_1.tct("All events have a fingerprint. Events with the same fingerprint are grouped together into an issue. To learn more about issue grouping, [link: read the docs].", {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/"/>),
            })}
        </textBlock_1.default>

        <form_1.default saveOnBlur allowUndo initialData={project} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmit}>
          <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Fingerprint Rules')} fields={[projectIssueGrouping_1.fields.fingerprintingRules]}/>

          <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Stack Trace Rules')} fields={[projectIssueGrouping_1.fields.groupingEnhancements]}/>

          <feature_1.default features={['set-grouping-config']} organization={organization}>
            <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Change defaults')} fields={[
                projectIssueGrouping_1.fields.groupingConfig,
                projectIssueGrouping_1.fields.secondaryGroupingConfig,
                projectIssueGrouping_1.fields.secondaryGroupingExpiry,
            ]}/>
          </feature_1.default>

          <upgradeGrouping_1.default groupingConfigs={groupingConfigs !== null && groupingConfigs !== void 0 ? groupingConfigs : []} organization={organization} projectId={params.projectId} project={project} api={this.api} onUpgrade={this.fetchData}/>
        </form_1.default>
      </react_1.Fragment>);
    };
    return ProjectDebugSymbols;
}(asyncView_1.default));
exports.default = ProjectDebugSymbols;
//# sourceMappingURL=index.jsx.map