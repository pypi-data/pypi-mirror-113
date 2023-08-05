Object.defineProperty(exports, "__esModule", { value: true });
exports.EmailAddresses = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var accountEmails_1 = tslib_1.__importDefault(require("app/data/forms/accountEmails"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var ENDPOINT = '/users/me/emails/';
var AccountEmails = /** @class */ (function (_super) {
    tslib_1.__extends(AccountEmails, _super);
    function AccountEmails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function (_change, model, id) {
            if (id === undefined) {
                return;
            }
            model.setValue(id, '');
            _this.remountComponent();
        };
        return _this;
    }
    AccountEmails.prototype.getTitle = function () {
        return locale_1.t('Emails');
    };
    AccountEmails.prototype.getEndpoints = function () {
        return [];
    };
    AccountEmails.prototype.renderBody = function () {
        return (<React.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Email Addresses')}/>
        <EmailAddresses />
        <form_1.default apiMethod="POST" apiEndpoint={ENDPOINT} saveOnBlur allowUndo={false} onSubmitSuccess={this.handleSubmitSuccess}>
          <jsonForm_1.default forms={accountEmails_1.default}/>
        </form_1.default>

        <alertLink_1.default to="/settings/account/notifications" icon={<icons_1.IconStack />}>
          {locale_1.t('Want to change how many emails you get? Use the notifications panel.')}
        </alertLink_1.default>
      </React.Fragment>);
    };
    return AccountEmails;
}(asyncView_1.default));
exports.default = AccountEmails;
var EmailAddresses = /** @class */ (function (_super) {
    tslib_1.__extends(EmailAddresses, _super);
    function EmailAddresses() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSetPrimary = function (email) {
            return _this.doApiCall(ENDPOINT, {
                method: 'PUT',
                data: { email: email },
            });
        };
        _this.handleRemove = function (email) {
            return _this.doApiCall(ENDPOINT, {
                method: 'DELETE',
                data: { email: email },
            });
        };
        _this.handleVerify = function (email) {
            return _this.doApiCall(ENDPOINT + "confirm/", {
                method: 'POST',
                data: { email: email },
            });
        };
        return _this;
    }
    EmailAddresses.prototype.getEndpoints = function () {
        return [['emails', ENDPOINT]];
    };
    EmailAddresses.prototype.doApiCall = function (endpoint, requestParams) {
        var _this = this;
        this.setState({ loading: true, emails: [] }, function () {
            return _this.api
                .requestPromise(endpoint, requestParams)
                .then(function () { return _this.remountComponent(); })
                .catch(function (err) {
                var _a;
                _this.remountComponent();
                if ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.email) {
                    indicator_1.addErrorMessage(err.responseJSON.email);
                }
            });
        });
    };
    EmailAddresses.prototype.render = function () {
        var _this = this;
        var _a = this.state, emails = _a.emails, loading = _a.loading;
        var primary = emails === null || emails === void 0 ? void 0 : emails.find(function (_a) {
            var isPrimary = _a.isPrimary;
            return isPrimary;
        });
        var secondary = emails === null || emails === void 0 ? void 0 : emails.filter(function (_a) {
            var isPrimary = _a.isPrimary;
            return !isPrimary;
        });
        if (loading) {
            return (<panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Email Addresses')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <loadingIndicator_1.default />
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Email Addresses')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          {primary && (<EmailRow onRemove={this.handleRemove} onVerify={this.handleVerify} {...primary}/>)}

          {secondary === null || secondary === void 0 ? void 0 : secondary.map(function (emailObj) { return (<EmailRow key={emailObj.email} onSetPrimary={_this.handleSetPrimary} onRemove={_this.handleRemove} onVerify={_this.handleVerify} {...emailObj}/>); })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return EmailAddresses;
}(asyncComponent_1.default));
exports.EmailAddresses = EmailAddresses;
var EmailRow = function (_a) {
    var email = _a.email, onRemove = _a.onRemove, onVerify = _a.onVerify, onSetPrimary = _a.onSetPrimary, isVerified = _a.isVerified, isPrimary = _a.isPrimary, hideRemove = _a.hideRemove;
    return (<EmailItem>
    <EmailTags>
      {email}
      {!isVerified && <tag_1.default type="warning">{locale_1.t('Unverified')}</tag_1.default>}
      {isPrimary && <tag_1.default type="success">{locale_1.t('Primary')}</tag_1.default>}
    </EmailTags>
    <buttonBar_1.default gap={1}>
      {!isPrimary && isVerified && (<button_1.default size="small" onClick={function (e) { return onSetPrimary === null || onSetPrimary === void 0 ? void 0 : onSetPrimary(email, e); }}>
          {locale_1.t('Set as primary')}
        </button_1.default>)}
      {!isVerified && (<button_1.default size="small" onClick={function (e) { return onVerify(email, e); }}>
          {locale_1.t('Resend verification')}
        </button_1.default>)}
      {!hideRemove && !isPrimary && (<button_1.default label={locale_1.t('Remove email')} data-test-id="remove" priority="danger" size="small" icon={<icons_1.IconDelete />} onClick={function (e) { return onRemove(email, e); }}/>)}
    </buttonBar_1.default>
  </EmailItem>);
};
var EmailTags = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(1));
var EmailItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  justify-content: space-between;\n"], ["\n  justify-content: space-between;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=accountEmails.jsx.map