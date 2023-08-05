Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var react_router_1 = require("react-router");
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var apiForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/apiForm"));
var multipleCheckbox_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/multipleCheckbox"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var SORTED_DEFAULT_API_ACCESS_SCOPES = constants_1.DEFAULT_API_ACCESS_SCOPES.sort();
var API_CHOICES = constants_1.API_ACCESS_SCOPES.map(function (s) { return [s, s]; });
var API_INDEX_ROUTE = '/settings/account/api/auth-tokens/';
var ApiNewToken = /** @class */ (function (_super) {
    tslib_1.__extends(ApiNewToken, _super);
    function ApiNewToken() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onCancel = function () {
            react_router_1.browserHistory.push(API_INDEX_ROUTE);
        };
        _this.onSubmitSuccess = function () {
            react_router_1.browserHistory.push(API_INDEX_ROUTE);
        };
        return _this;
    }
    ApiNewToken.prototype.render = function () {
        return (<react_document_title_1.default title="Create API Token - Sentry">
        <div>
          <settingsPageHeader_1.default title={locale_1.t('Create New Token')}/>
          <textBlock_1.default>
            {locale_1.t("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API.")}
          </textBlock_1.default>
          <textBlock_1.default>
            {locale_1.tct('For more information on how to use the web API, see our [link:documentation].', {
                link: <a href="https://docs.sentry.io/api/"/>,
            })}
          </textBlock_1.default>
          <panels_1.Panel>
            <panels_1.PanelHeader>{locale_1.t('Create New Token')}</panels_1.PanelHeader>
            <apiForm_1.default apiMethod="POST" apiEndpoint="/api-tokens/" initialData={{ scopes: SORTED_DEFAULT_API_ACCESS_SCOPES }} onSubmitSuccess={this.onSubmitSuccess} onCancel={this.onCancel} footerStyle={{
                marginTop: 0,
                paddingRight: 20,
            }} submitLabel={locale_1.t('Create Token')}>
              <panels_1.PanelBody>
                <formField_1.default name="scopes" label={locale_1.t('Scopes')} inline={false} required>
                  {function (_a) {
                var value = _a.value, onChange = _a.onChange;
                return (<multipleCheckbox_1.default onChange={onChange} value={value} choices={API_CHOICES}/>);
            }}
                </formField_1.default>
              </panels_1.PanelBody>
            </apiForm_1.default>
          </panels_1.Panel>
        </div>
      </react_document_title_1.default>);
    };
    return ApiNewToken;
}(react_1.Component));
exports.default = ApiNewToken;
//# sourceMappingURL=apiNewToken.jsx.map