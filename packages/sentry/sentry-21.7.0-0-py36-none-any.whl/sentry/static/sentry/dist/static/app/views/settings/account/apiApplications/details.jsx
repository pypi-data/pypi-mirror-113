Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var panels_1 = require("app/components/panels");
var apiApplication_1 = tslib_1.__importDefault(require("app/data/forms/apiApplication"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var ApiApplicationsDetails = /** @class */ (function (_super) {
    tslib_1.__extends(ApiApplicationsDetails, _super);
    function ApiApplicationsDetails() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ApiApplicationsDetails.prototype.getEndpoints = function () {
        return [['app', "/api-applications/" + this.props.params.appId + "/"]];
    };
    ApiApplicationsDetails.prototype.getTitle = function () {
        return locale_1.t('Application Details');
    };
    ApiApplicationsDetails.prototype.renderBody = function () {
        var urlPrefix = configStore_1.default.get('urlPrefix');
        return (<div>
        <settingsPageHeader_1.default title={this.getTitle()}/>

        <form_1.default apiMethod="PUT" apiEndpoint={"/api-applications/" + this.props.params.appId + "/"} saveOnBlur allowUndo initialData={this.state.app} onSubmitError={function () { return indicator_1.addErrorMessage('Unable to save change'); }}>
          <jsonForm_1.default forms={apiApplication_1.default}/>

          <panels_1.Panel>
            <panels_1.PanelHeader>{locale_1.t('Credentials')}</panels_1.PanelHeader>

            <panels_1.PanelBody>
              <formField_1.default name="clientID" label="Client ID">
                {function (_a) {
                var value = _a.value;
                return (<div>
                    <textCopyInput_1.default>
                      {getDynamicText_1.default({ value: value, fixed: 'CI_CLIENT_ID' })}
                    </textCopyInput_1.default>
                  </div>);
            }}
              </formField_1.default>

              <formField_1.default name="clientSecret" label="Client Secret" help={locale_1.t("Your secret is only available briefly after application creation. Make\n                  sure to save this value!")}>
                {function (_a) {
                var value = _a.value;
                return value ? (<textCopyInput_1.default>
                      {getDynamicText_1.default({ value: value, fixed: 'CI_CLIENT_SECRET' })}
                    </textCopyInput_1.default>) : (<em>hidden</em>);
            }}
              </formField_1.default>

              <formField_1.default name="" label="Authorization URL">
                {function () { return <textCopyInput_1.default>{urlPrefix + "/oauth/authorize/"}</textCopyInput_1.default>; }}
              </formField_1.default>

              <formField_1.default name="" label="Token URL">
                {function () { return <textCopyInput_1.default>{urlPrefix + "/oauth/token/"}</textCopyInput_1.default>; }}
              </formField_1.default>
            </panels_1.PanelBody>
          </panels_1.Panel>
        </form_1.default>
      </div>);
    };
    return ApiApplicationsDetails;
}(asyncView_1.default));
exports.default = ApiApplicationsDetails;
//# sourceMappingURL=details.jsx.map