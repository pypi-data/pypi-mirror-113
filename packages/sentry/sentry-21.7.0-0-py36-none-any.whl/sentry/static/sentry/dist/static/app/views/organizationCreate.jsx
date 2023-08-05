Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var forms_1 = require("app/components/forms");
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var OrganizationCreate = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationCreate, _super);
    function OrganizationCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onSubmitSuccess = function (data) {
            // redirect to project creation *(BYPASS REACT ROUTER AND FORCE PAGE REFRESH TO GRAB CSRF TOKEN)*
            // browserHistory.pushState(null, `/organizations/${data.slug}/projects/new/`);
            window.location.href = "/organizations/" + data.slug + "/projects/new/";
        };
        return _this;
    }
    OrganizationCreate.prototype.getEndpoints = function () {
        return [];
    };
    OrganizationCreate.prototype.getTitle = function () {
        return locale_1.t('Create Organization');
    };
    OrganizationCreate.prototype.renderBody = function () {
        var termsUrl = configStore_1.default.get('termsUrl');
        var privacyUrl = configStore_1.default.get('privacyUrl');
        return (<narrowLayout_1.default showLogout>
        <h3>{locale_1.t('Create a New Organization')}</h3>

        <p>
          {locale_1.t("Organizations represent the top level in your hierarchy. You'll be able to bundle a collection of teams within an organization as well as give organization-wide permissions to users.")}
        </p>

        <forms_1.ApiForm initialData={{ defaultTeam: true }} submitLabel={locale_1.t('Create Organization')} apiEndpoint="/organizations/" apiMethod="POST" onSubmitSuccess={this.onSubmitSuccess} requireChanges>
          <forms_1.TextField name="name" label={locale_1.t('Organization Name')} placeholder={locale_1.t('e.g. My Company')} required/>

          {termsUrl && privacyUrl && (<forms_1.BooleanField name="agreeTerms" label={locale_1.tct('I agree to the [termsLink:Terms of Service] and the [privacyLink:Privacy Policy]', {
                    termsLink: <a href={termsUrl}/>,
                    privacyLink: <a href={privacyUrl}/>,
                })} required/>)}
        </forms_1.ApiForm>
      </narrowLayout_1.default>);
    };
    return OrganizationCreate;
}(asyncView_1.default));
exports.default = OrganizationCreate;
//# sourceMappingURL=organizationCreate.jsx.map