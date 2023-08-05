Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var projectSecurityAndPrivacyGroups_1 = tslib_1.__importDefault(require("app/data/forms/projectSecurityAndPrivacyGroups"));
var locale_1 = require("app/locale");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var dataScrubbing_1 = tslib_1.__importDefault(require("../components/dataScrubbing"));
var ProjectSecurityAndPrivacy = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectSecurityAndPrivacy, _super);
    function ProjectSecurityAndPrivacy() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateProject = function (data) {
            // This will update our project global state
            projectActions_1.default.updateSuccess(data);
        };
        return _this;
    }
    ProjectSecurityAndPrivacy.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var initialData = project;
        var projectSlug = project.slug;
        var endpoint = "/projects/" + organization.slug + "/" + projectSlug + "/";
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        var relayPiiConfig = project.relayPiiConfig;
        var apiMethod = 'PUT';
        var title = locale_1.t('Security & Privacy');
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectSlug}/>
        <settingsPageHeader_1.default title={title}/>
        <form_1.default saveOnBlur allowUndo initialData={initialData} apiMethod={apiMethod} apiEndpoint={endpoint} onSubmitSuccess={this.handleUpdateProject} onSubmitError={function () { return indicator_1.addErrorMessage('Unable to save change'); }}>
          <jsonForm_1.default additionalFieldProps={{ organization: organization }} features={features} disabled={!access.has('project:write')} forms={projectSecurityAndPrivacyGroups_1.default}/>
        </form_1.default>
        <dataScrubbing_1.default additionalContext={<span>
              {locale_1.tct('These rules can be configured at the organization level in [linkToOrganizationSecurityAndPrivacy].', {
                    linkToOrganizationSecurityAndPrivacy: (<link_1.default to={"/settings/" + organization.slug + "/security-and-privacy/"}>
                      {title}
                    </link_1.default>),
                })}
            </span>} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('project:write')} organization={organization} projectId={project.id} onSubmitSuccess={this.handleUpdateProject}/>
      </react_1.Fragment>);
    };
    return ProjectSecurityAndPrivacy;
}(react_1.Component));
exports.default = ProjectSecurityAndPrivacy;
//# sourceMappingURL=index.jsx.map