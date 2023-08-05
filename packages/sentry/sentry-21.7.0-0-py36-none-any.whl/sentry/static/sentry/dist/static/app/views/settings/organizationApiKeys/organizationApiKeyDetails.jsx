Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var indicator_1 = require("app/actionCreators/indicator");
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var apiForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/apiForm"));
var multipleCheckbox_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/multipleCheckbox"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var textareaField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textareaField"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var API_CHOICES = constants_1.API_ACCESS_SCOPES.map(function (s) { return [s, s]; });
var OrganizationApiKeyDetails = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationApiKeyDetails, _super);
    function OrganizationApiKeyDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            indicator_1.addSuccessMessage('Saved changes');
            // Go back to API list
            react_router_1.browserHistory.push(recreateRoute_1.default('', {
                stepBack: -1,
                routes: _this.props.routes,
                params: _this.props.params,
            }));
        };
        _this.handleSubmitError = function () {
            indicator_1.addErrorMessage('Unable to save changes. Please try again.');
        };
        return _this;
    }
    OrganizationApiKeyDetails.prototype.getEndpoints = function () {
        return [
            [
                'apiKey',
                "/organizations/" + this.props.params.orgId + "/api-keys/" + this.props.params.apiKey + "/",
            ],
        ];
    };
    OrganizationApiKeyDetails.prototype.getTitle = function () {
        return routeTitle_1.default(locale_1.t('Edit API Key'), this.props.organization.slug, false);
    };
    OrganizationApiKeyDetails.prototype.renderBody = function () {
        var _this = this;
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Edit API Key')}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('API Key')}</panels_1.PanelHeader>
          <apiForm_1.default apiMethod="PUT" apiEndpoint={"/organizations/" + this.props.params.orgId + "/api-keys/" + this.props.params.apiKey + "/"} initialData={this.state.apiKey} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onCancel={function () {
                return react_router_1.browserHistory.push(recreateRoute_1.default('', {
                    stepBack: -1,
                    routes: _this.props.routes,
                    params: _this.props.params,
                }));
            }}>
            <panels_1.PanelBody>
              <textField_1.default label={locale_1.t('Label')} name="label"/>
              <textField_1.default label={locale_1.t('API Key')} name="key" disabled/>

              <formField_1.default name="scope_list" label={locale_1.t('Scopes')} inline={false} required>
                {function (_a) {
                var value = _a.value, onChange = _a.onChange;
                return (<multipleCheckbox_1.default value={value} onChange={onChange} choices={API_CHOICES}/>);
            }}
              </formField_1.default>

              <textareaField_1.default label={locale_1.t('Allowed Domains')} name="allowed_origins" placeholder="e.g. example.com or https://example.com" help="Separate multiple entries with a newline"/>
            </panels_1.PanelBody>
          </apiForm_1.default>
        </panels_1.Panel>
      </div>);
    };
    return OrganizationApiKeyDetails;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationApiKeyDetails);
//# sourceMappingURL=organizationApiKeyDetails.jsx.map