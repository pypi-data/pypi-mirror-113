Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var BYE_URL = '/';
var leaveRedirect = function () { return (window.location.href = BYE_URL); };
var Important = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  font-size: 1.2em;\n"], ["\n  font-weight: bold;\n  font-size: 1.2em;\n"])));
var GoodbyeModalContent = function (_a) {
    var Header = _a.Header, Body = _a.Body, Footer = _a.Footer;
    return (<div>
    <Header>{locale_1.t('Closing Account')}</Header>
    <Body>
      <textBlock_1.default>
        {locale_1.t('Your account has been deactivated and scheduled for removal.')}
      </textBlock_1.default>
      <textBlock_1.default>
        {locale_1.t('Thanks for using Sentry! We hope to see you again soon!')}
      </textBlock_1.default>
    </Body>
    <Footer>
      <button_1.default href={BYE_URL}>{locale_1.t('Goodbye')}</button_1.default>
    </Footer>
  </div>);
};
var AccountClose = /** @class */ (function (_super) {
    tslib_1.__extends(AccountClose, _super);
    function AccountClose() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (_a, isSingle, event) {
            var slug = _a.slug;
            var checked = event.target.checked;
            // Can't unselect an org where you are the single owner
            if (isSingle) {
                return;
            }
            _this.setState(function (state) {
                var set = state.orgsToRemove || new Set(_this.singleOwnerOrgs);
                if (checked) {
                    set.add(slug);
                }
                else {
                    set.delete(slug);
                }
                return { orgsToRemove: set };
            });
        };
        _this.handleRemoveAccount = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var orgsToRemove, orgs, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        orgsToRemove = this.state.orgsToRemove;
                        orgs = orgsToRemove === null ? this.singleOwnerOrgs : Array.from(orgsToRemove);
                        indicator_1.addLoadingMessage('Closing account\u2026');
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise('/users/me/', {
                                method: 'DELETE',
                                data: { organizations: orgs },
                            })];
                    case 2:
                        _b.sent();
                        modal_1.openModal(GoodbyeModalContent, {
                            onClose: leaveRedirect,
                        });
                        // Redirect after 10 seconds
                        setTimeout(leaveRedirect, 10000);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage('Error closing account');
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountClose.prototype.getEndpoints = function () {
        return [['organizations', '/organizations/?owner=1']];
    };
    AccountClose.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { orgsToRemove: null });
    };
    Object.defineProperty(AccountClose.prototype, "singleOwnerOrgs", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.state.organizations) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                var singleOwner = _a.singleOwner;
                return singleOwner;
            })) === null || _b === void 0 ? void 0 : _b.map(function (_a) {
                var organization = _a.organization;
                return organization.slug;
            });
        },
        enumerable: false,
        configurable: true
    });
    AccountClose.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, organizations = _a.organizations, orgsToRemove = _a.orgsToRemove;
        return (<div>
        <settingsPageHeader_1.default title="Close Account"/>

        <textBlock_1.default>
          {locale_1.t('This will permanently remove all associated data for your user')}.
        </textBlock_1.default>

        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          <Important>
            {locale_1.t('Closing your account is permanent and cannot be undone')}!
          </Important>
        </alert_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Remove the following organizations')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <panels_1.PanelAlert type="info">
              {locale_1.t('Ownership will remain with other organization owners if an organization is not deleted.')}
              <br />
              {locale_1.tct("Boxes which can't be unchecked mean that you are the only organization owner and the organization [strong:will be deleted].", { strong: <strong /> })}
            </panels_1.PanelAlert>

            {organizations === null || organizations === void 0 ? void 0 : organizations.map(function (_a) {
                var organization = _a.organization, singleOwner = _a.singleOwner;
                return (<panels_1.PanelItem key={organization.slug}>
                <label>
                  <input style={{ marginRight: 6 }} type="checkbox" value={organization.slug} onChange={_this.handleChange.bind(_this, organization, singleOwner)} name="organizations" checked={orgsToRemove === null
                        ? singleOwner
                        : orgsToRemove.has(organization.slug)} disabled={singleOwner}/>
                  {organization.slug}
                </label>
              </panels_1.PanelItem>);
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <confirm_1.default priority="danger" message={locale_1.t('This is permanent and cannot be undone, are you really sure you want to do this?')} onConfirm={this.handleRemoveAccount}>
          <button_1.default priority="danger">{locale_1.t('Close Account')}</button_1.default>
        </confirm_1.default>
      </div>);
    };
    return AccountClose;
}(asyncView_1.default));
exports.default = AccountClose;
var templateObject_1;
//# sourceMappingURL=accountClose.jsx.map