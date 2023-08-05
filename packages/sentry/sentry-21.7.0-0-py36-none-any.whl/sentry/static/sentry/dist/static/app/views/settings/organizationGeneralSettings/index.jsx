Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var indicator_1 = require("app/actionCreators/indicator");
var organizations_1 = require("app/actionCreators/organizations");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/organization/permissionAlert"));
var organizationSettingsForm_1 = tslib_1.__importDefault(require("./organizationSettingsForm"));
var OrganizationGeneralSettings = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationGeneralSettings, _super);
    function OrganizationGeneralSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemoveOrganization = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, params = _a.params;
            if (!organization) {
                return;
            }
            indicator_1.addLoadingMessage();
            organizations_1.removeAndRedirectToRemainingOrganization(api, {
                orgId: params.orgId,
                successMessage: organization.name + " is queued for deletion.",
                errorMessage: "Error removing the " + organization.name + " organization",
            });
        };
        _this.handleSave = function (prevData, data) {
            if (data.slug && data.slug !== prevData.slug) {
                organizations_1.changeOrganizationSlug(prevData, data);
                react_router_1.browserHistory.replace("/settings/" + data.slug + "/");
            }
            else {
                // This will update OrganizationStore (as well as OrganizationsStore
                // which is slightly incorrect because it has summaries vs a detailed org)
                organizations_1.updateOrganization(data);
            }
        };
        return _this;
    }
    OrganizationGeneralSettings.prototype.render = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var orgId = params.orgId;
        var access = new Set(organization.access);
        var hasProjects = organization.projects && !!organization.projects.length;
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={locale_1.t('General Settings')} orgSlug={orgId}/>
        <div>
          <settingsPageHeader_1.default title={locale_1.t('Organization Settings')}/>
          <permissionAlert_1.default />

          <organizationSettingsForm_1.default {...this.props} initialData={organization} access={access} onSave={this.handleSave}/>

          {access.has('org:admin') && !organization.isDefault && (<panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Remove Organization')}</panels_1.PanelHeader>
              <field_1.default label={locale_1.t('Remove Organization')} help={locale_1.t('Removing this organization will delete all data including projects and their associated events.')}>
                <div>
                  <confirm_1.default priority="danger" confirmText={locale_1.t('Remove Organization')} message={<div>
                        <textBlock_1.default>
                          {locale_1.tct('Removing the organization, [name] is permanent and cannot be undone! Are you sure you want to continue?', {
                        name: organization && <strong>{organization.name}</strong>,
                    })}
                        </textBlock_1.default>

                        {hasProjects && (<div>
                            <textBlock_1.default noMargin>
                              {locale_1.t('This will also remove the following associated projects:')}
                            </textBlock_1.default>
                            <ul className="ref-projects">
                              {organization.projects.map(function (project) { return (<li key={project.slug}>{project.slug}</li>); })}
                            </ul>
                          </div>)}
                      </div>} onConfirm={this.handleRemoveOrganization}>
                    <button_1.default priority="danger" title={locale_1.t('Remove %s organization', organization && organization.name)}>
                      {locale_1.t('Remove Organization')}
                    </button_1.default>
                  </confirm_1.default>
                </div>
              </field_1.default>
            </panels_1.Panel>)}
        </div>
      </react_1.Fragment>);
    };
    return OrganizationGeneralSettings;
}(react_1.Component));
exports.default = withApi_1.default(withOrganization_1.default(OrganizationGeneralSettings));
//# sourceMappingURL=index.jsx.map