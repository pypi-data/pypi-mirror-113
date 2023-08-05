var _a;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var accountNotificationSettings_1 = tslib_1.__importDefault(require("app/data/forms/accountNotificationSettings"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var notificationSettings_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettings"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var FINE_TUNE_FOOTERS = (_a = {},
    _a[locale_1.t('Alerts')] = {
        text: locale_1.t('Fine tune alerts by project'),
        path: 'alerts/',
    },
    _a[locale_1.t('Workflow Notifications')] = {
        text: locale_1.t('Fine tune workflow notifications by project'),
        path: 'workflow/',
    },
    _a[locale_1.t('Email Routing')] = {
        text: locale_1.t('Fine tune email routing by project'),
        path: 'email/',
    },
    _a[locale_1.t('Weekly Reports')] = {
        text: locale_1.t('Fine tune weekly reports by organization'),
        path: 'reports/',
    },
    _a[locale_1.t('Deploy Notifications')] = {
        text: locale_1.t('Fine tune deploy notifications by organization'),
        path: 'deploy/',
    },
    _a);
var AccountNotifications = /** @class */ (function (_super) {
    tslib_1.__extends(AccountNotifications, _super);
    function AccountNotifications() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountNotifications.prototype.getEndpoints = function () {
        return [['data', '/users/me/notifications/']];
    };
    AccountNotifications.prototype.getTitle = function () {
        return 'Notifications';
    };
    AccountNotifications.prototype.renderBody = function () {
        var _a;
        var organizations = this.props.organizations;
        if (organizations.some(function (organization) {
            return organization.features.includes('notification-platform');
        })) {
            return <notificationSettings_1.default />;
        }
        return (<div>
        <settingsPageHeader_1.default title="Notifications"/>
        <form_1.default initialData={(_a = this.state.data) !== null && _a !== void 0 ? _a : undefined} saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/">
          <jsonForm_1.default forms={accountNotificationSettings_1.default} renderFooter={function (_a) {
                var title = _a.title;
                if (typeof title !== 'string') {
                    return null;
                }
                if (FINE_TUNE_FOOTERS[title]) {
                    return <FineTuningFooter {...FINE_TUNE_FOOTERS[title]}/>;
                }
                return null;
            }}/>
          <alertLink_1.default to="/settings/account/emails" icon={<icons_1.IconMail />}>
            {locale_1.t('Looking to add or remove an email address? Use the emails panel.')}
          </alertLink_1.default>
        </form_1.default>
      </div>);
    };
    return AccountNotifications;
}(asyncView_1.default));
var FineTuneLink = styled_1.default(link_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  padding: 15px 20px;\n  color: inherit;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  padding: 15px 20px;\n  color: inherit;\n"])));
var FineTuningFooter = function (_a) {
    var path = _a.path, text = _a.text;
    return (<panels_1.PanelFooter css={{ borderTop: 'none' }}>
    <FineTuneLink to={"/settings/account/notifications/" + path}>
      <span>{text}</span>
      <icons_1.IconChevron direction="right" size="15px"/>
    </FineTuneLink>
  </panels_1.PanelFooter>);
};
exports.default = withOrganizations_1.default(AccountNotifications);
var templateObject_1;
//# sourceMappingURL=accountNotifications.jsx.map