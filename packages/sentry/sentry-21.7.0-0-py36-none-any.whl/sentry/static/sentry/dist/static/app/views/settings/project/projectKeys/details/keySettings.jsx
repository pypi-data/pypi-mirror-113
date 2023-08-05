Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var booleanField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/booleanField"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var keyRateLimitsForm_1 = tslib_1.__importDefault(require("app/views/settings/project/projectKeys/details/keyRateLimitsForm"));
var projectKeyCredentials_1 = tslib_1.__importDefault(require("app/views/settings/project/projectKeys/projectKeyCredentials"));
var KeySettings = /** @class */ (function (_super) {
    tslib_1.__extends(KeySettings, _super);
    function KeySettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            error: false,
        };
        _this.handleRemove = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, onRemove, params, keyId, orgId, projectId, _err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (this.state.loading) {
                            return [2 /*return*/];
                        }
                        indicator_1.addLoadingMessage(locale_1.t('Revoking key\u2026'));
                        _a = this.props, api = _a.api, onRemove = _a.onRemove, params = _a.params;
                        keyId = params.keyId, orgId = params.orgId, projectId = params.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        onRemove();
                        indicator_1.addSuccessMessage(locale_1.t('Revoked key'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        this.setState({
                            error: true,
                            loading: false,
                        });
                        indicator_1.addErrorMessage(locale_1.t('Unable to revoke key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    KeySettings.prototype.render = function () {
        var _this = this;
        var _a = this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
        var data = this.props.data;
        var apiEndpoint = "/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/";
        var loaderLink = getDynamicText_1.default({
            value: data.dsn.cdn,
            fixed: '__JS_SDK_LOADER_URL__',
        });
        return (<access_1.default access={['project:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<react_1.Fragment>
            <form_1.default saveOnBlur allowUndo apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
              <panels_1.Panel>
                <panels_1.PanelHeader>{locale_1.t('Details')}</panels_1.PanelHeader>

                <panels_1.PanelBody>
                  <textField_1.default name="name" label={locale_1.t('Name')} disabled={!hasAccess} required={false} maxLength={64}/>
                  <booleanField_1.default name="isActive" label={locale_1.t('Enabled')} required={false} disabled={!hasAccess} help="Accept events from this key? This may be used to temporarily suspend a key."/>
                  <field_1.default label={locale_1.t('Created')}>
                    <div className="controls">
                      <dateTime_1.default date={data.dateCreated}/>
                    </div>
                  </field_1.default>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </form_1.default>

            <keyRateLimitsForm_1.default params={_this.props.params} data={data} disabled={!hasAccess}/>

            <form_1.default saveOnBlur apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
              <panels_1.Panel>
                <panels_1.PanelHeader>{locale_1.t('JavaScript Loader')}</panels_1.PanelHeader>
                <panels_1.PanelBody>
                  <field_1.default help={locale_1.tct('Copy this script into your website to setup your JavaScript SDK without any additional configuration. [link]', {
                        link: (<externalLink_1.default href="https://docs.sentry.io/platforms/javascript/install/lazy-load-sentry/">
                            What does the script provide?
                          </externalLink_1.default>),
                    })} inline={false} flexibleControlStateSize>
                    <textCopyInput_1.default>
                      {"<script src='" + loaderLink + "' crossorigin=\"anonymous\"></script>"}
                    </textCopyInput_1.default>
                  </field_1.default>
                  <selectField_1.default name="browserSdkVersion" choices={data.browserSdk ? data.browserSdk.choices : []} placeholder={locale_1.t('4.x')} allowClear={false} enabled={!hasAccess} help={locale_1.t('Select the version of the SDK that should be loaded. Note that it can take a few minutes until this change is live.')}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </form_1.default>

            <panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Credentials')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
                  {locale_1.t('Your credentials are coupled to a public and secret key. Different clients will require different credentials, so make sure you check the documentation before plugging things in.')}
                </panels_1.PanelAlert>

                <projectKeyCredentials_1.default projectId={"" + data.projectId} data={data} showPublicKey showSecretKey showProjectId/>
              </panels_1.PanelBody>
            </panels_1.Panel>

            <access_1.default access={['project:admin']}>
              <panels_1.Panel>
                <panels_1.PanelHeader>{locale_1.t('Revoke Key')}</panels_1.PanelHeader>
                <panels_1.PanelBody>
                  <field_1.default label={locale_1.t('Revoke Key')} help={locale_1.t('Revoking this key will immediately remove and suspend the credentials. This action is irreversible.')}>
                    <div>
                      <confirm_1.default priority="danger" message={locale_1.t('Are you sure you want to revoke this key? This will immediately remove and suspend the credentials.')} onConfirm={_this.handleRemove} confirmText={locale_1.t('Revoke Key')}>
                        <button_1.default priority="danger">{locale_1.t('Revoke Key')}</button_1.default>
                      </confirm_1.default>
                    </div>
                  </field_1.default>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </access_1.default>
          </react_1.Fragment>);
            }}
      </access_1.default>);
    };
    return KeySettings;
}(react_1.Component));
exports.default = KeySettings;
//# sourceMappingURL=keySettings.jsx.map