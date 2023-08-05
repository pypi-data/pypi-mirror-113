Object.defineProperty(exports, "__esModule", { value: true });
exports.ApiTokens = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var apiTokenRow_1 = tslib_1.__importDefault(require("app/views/settings/account/apiTokenRow"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var ApiTokens = /** @class */ (function (_super) {
    tslib_1.__extends(ApiTokens, _super);
    function ApiTokens() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemoveToken = function (token) {
            indicator_1.addLoadingMessage();
            var oldTokenList = _this.state.tokenList;
            _this.setState(function (state) {
                var _a, _b;
                return ({
                    tokenList: (_b = (_a = state.tokenList) === null || _a === void 0 ? void 0 : _a.filter(function (tk) { return tk.token !== token.token; })) !== null && _b !== void 0 ? _b : [],
                });
            }, function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _err_1;
                return tslib_1.__generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            return [4 /*yield*/, this.api.requestPromise('/api-tokens/', {
                                    method: 'DELETE',
                                    data: { token: token.token },
                                })];
                        case 1:
                            _a.sent();
                            indicator_1.addSuccessMessage(locale_1.t('Removed token'));
                            return [3 /*break*/, 3];
                        case 2:
                            _err_1 = _a.sent();
                            indicator_1.addErrorMessage(locale_1.t('Unable to remove token. Please try again.'));
                            this.setState({
                                tokenList: oldTokenList,
                            });
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); });
        };
        return _this;
    }
    ApiTokens.prototype.getTitle = function () {
        return locale_1.t('API Tokens');
    };
    ApiTokens.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { tokenList: [] });
    };
    ApiTokens.prototype.getEndpoints = function () {
        return [['tokenList', '/api-tokens/']];
    };
    ApiTokens.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var organization = this.props.organization;
        var tokenList = this.state.tokenList;
        var isEmpty = !Array.isArray(tokenList) || tokenList.length === 0;
        var action = (<button_1.default priority="primary" size="small" to="/settings/account/api/auth-tokens/new-token/" data-test-id="create-token">
        {locale_1.t('Create New Token')}
      </button_1.default>);
        return (<div>
        <settingsPageHeader_1.default title="Auth Tokens" action={action}/>
        <alertLink_1.default to={"/settings/" + ((_a = organization === null || organization === void 0 ? void 0 : organization.slug) !== null && _a !== void 0 ? _a : '') + "/developer-settings/new-internal"}>
          {locale_1.t("Auth Tokens are tied to the logged in user, meaning they'll stop working if the user leaves the organization! We suggest using internal integrations to create/manage tokens tied to the organization instead.")}
        </alertLink_1.default>
        <textBlock_1.default>
          {locale_1.t("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API.")}
        </textBlock_1.default>
        <textBlock_1.default>
          {locale_1.tct('For more information on how to use the web API, see our [link:documentation].', {
                link: <a href="https://docs.sentry.io/api/"/>,
            })}
        </textBlock_1.default>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Auth Token')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            {isEmpty && (<emptyMessage_1.default>
                {locale_1.t("You haven't created any authentication tokens yet.")}
              </emptyMessage_1.default>)}

            {tokenList === null || tokenList === void 0 ? void 0 : tokenList.map(function (token) { return (<apiTokenRow_1.default key={token.token} token={token} onRemove={_this.handleRemoveToken}/>); })}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return ApiTokens;
}(asyncView_1.default));
exports.ApiTokens = ApiTokens;
exports.default = withOrganization_1.default(ApiTokens);
//# sourceMappingURL=apiTokens.jsx.map