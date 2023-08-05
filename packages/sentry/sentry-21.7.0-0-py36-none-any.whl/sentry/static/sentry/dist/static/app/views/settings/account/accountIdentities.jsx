Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var account_1 = require("app/actionCreators/account");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var ENDPOINT = '/users/me/social-identities/';
var AccountIdentities = /** @class */ (function (_super) {
    tslib_1.__extends(AccountIdentities, _super);
    function AccountIdentities() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisconnect = function (identity) {
            var identities = _this.state.identities;
            _this.setState(function (state) {
                var _a;
                var newIdentities = (_a = state.identities) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                    var id = _a.id;
                    return id !== identity.id;
                });
                return {
                    identities: newIdentities !== null && newIdentities !== void 0 ? newIdentities : [],
                };
            }, function () {
                return account_1.disconnectIdentity(identity).catch(function () {
                    _this.setState({
                        identities: identities,
                    });
                });
            });
        };
        return _this;
    }
    AccountIdentities.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { identities: [] });
    };
    AccountIdentities.prototype.getEndpoints = function () {
        return [['identities', ENDPOINT]];
    };
    AccountIdentities.prototype.getTitle = function () {
        return locale_1.t('Identities');
    };
    AccountIdentities.prototype.renderBody = function () {
        var _this = this;
        var _a;
        return (<div>
        <settingsPageHeader_1.default title="Identities"/>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Identities')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {!((_a = this.state.identities) === null || _a === void 0 ? void 0 : _a.length) ? (<emptyMessage_1.default>
                {locale_1.t('There are no identities associated with this account')}
              </emptyMessage_1.default>) : (this.state.identities.map(function (identity) { return (<IdentityPanelItem key={identity.id}>
                  <div>{identity.providerLabel}</div>

                  <button_1.default size="small" onClick={_this.handleDisconnect.bind(_this, identity)}>
                    {locale_1.t('Disconnect')}
                  </button_1.default>
                </IdentityPanelItem>); }))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return AccountIdentities;
}(asyncView_1.default));
var IdentityPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
exports.default = AccountIdentities;
var templateObject_1;
//# sourceMappingURL=accountIdentities.jsx.map