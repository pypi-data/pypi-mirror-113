Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var organizations_1 = require("app/actionCreators/organizations");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var avatarChooser_1 = tslib_1.__importDefault(require("app/components/avatarChooser"));
var organizationGeneralSettings_1 = tslib_1.__importDefault(require("app/data/forms/organizationGeneralSettings"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var OrganizationSettingsForm = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationSettingsForm, _super);
    function OrganizationSettingsForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationSettingsForm.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [['authProvider', "/organizations/" + organization.slug + "/auth-provider/"]];
    };
    OrganizationSettingsForm.prototype.render = function () {
        var _a = this.props, initialData = _a.initialData, organization = _a.organization, onSave = _a.onSave, access = _a.access;
        var authProvider = this.state.authProvider;
        var endpoint = "/organizations/" + organization.slug + "/";
        var jsonFormSettings = {
            additionalFieldProps: { hasSsoEnabled: !!authProvider },
            features: new Set(organization.features),
            access: access,
            location: this.props.location,
            disabled: !access.has('org:write'),
        };
        return (<form_1.default data-test-id="organization-settings" apiMethod="PUT" apiEndpoint={endpoint} saveOnBlur allowUndo initialData={initialData} onSubmitSuccess={function (_resp, model) {
                // Special case for slug, need to forward to new slug
                if (typeof onSave === 'function') {
                    onSave(initialData, model.initialData);
                }
            }} onSubmitError={function () { return indicator_1.addErrorMessage('Unable to save change'); }}>
        <jsonForm_1.default {...jsonFormSettings} forms={organizationGeneralSettings_1.default}/>
        <avatarChooser_1.default type="organization" allowGravatar={false} endpoint={endpoint + "avatar/"} model={initialData} onSave={organizations_1.updateOrganization} disabled={!access.has('org:write')}/>
      </form_1.default>);
    };
    return OrganizationSettingsForm;
}(asyncComponent_1.default));
exports.default = withOrganization_1.default(OrganizationSettingsForm);
//# sourceMappingURL=organizationSettingsForm.jsx.map