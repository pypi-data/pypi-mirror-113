Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var organizations_1 = require("app/actionCreators/organizations");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var organizationSecurityAndPrivacyGroups_1 = tslib_1.__importDefault(require("app/data/forms/organizationSecurityAndPrivacyGroups"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var dataScrubbing_1 = tslib_1.__importDefault(require("../components/dataScrubbing"));
var OrganizationSecurityAndPrivacyContent = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationSecurityAndPrivacyContent, _super);
    function OrganizationSecurityAndPrivacyContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateOrganization = function (data) {
            // This will update OrganizationStore (as well as OrganizationsStore
            // which is slightly incorrect because it has summaries vs a detailed org)
            organizations_1.updateOrganization(data);
        };
        return _this;
    }
    OrganizationSecurityAndPrivacyContent.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['authProvider', "/organizations/" + orgId + "/auth-provider/"]];
    };
    OrganizationSecurityAndPrivacyContent.prototype.renderBody = function () {
        var organization = this.props.organization;
        var orgId = this.props.params.orgId;
        var initialData = organization;
        var endpoint = "/organizations/" + orgId + "/";
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        var relayPiiConfig = organization.relayPiiConfig;
        var authProvider = this.state.authProvider;
        var title = locale_1.t('Security & Privacy');
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}/>
        <settingsPageHeader_1.default title={title}/>
        <form_1.default data-test-id="organization-settings-security-and-privacy" apiMethod="PUT" apiEndpoint={endpoint} initialData={initialData} additionalFieldProps={{ hasSsoEnabled: !!authProvider }} onSubmitSuccess={this.handleUpdateOrganization} onSubmitError={function () { return indicator_1.addErrorMessage(locale_1.t('Unable to save change')); }} saveOnBlur allowUndo>
          <jsonForm_1.default features={features} forms={organizationSecurityAndPrivacyGroups_1.default} disabled={!access.has('org:write')}/>
        </form_1.default>
        <dataScrubbing_1.default additionalContext={locale_1.t('These rules can be configured for each project.')} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('org:write')} organization={organization} onSubmitSuccess={this.handleUpdateOrganization}/>
      </react_1.Fragment>);
    };
    return OrganizationSecurityAndPrivacyContent;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationSecurityAndPrivacyContent);
//# sourceMappingURL=index.jsx.map