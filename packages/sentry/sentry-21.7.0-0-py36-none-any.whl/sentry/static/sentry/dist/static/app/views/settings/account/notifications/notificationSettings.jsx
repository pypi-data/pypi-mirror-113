Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var constants_1 = require("app/views/settings/account/notifications/constants");
var feedbackAlert_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/feedbackAlert"));
var fields2_1 = require("app/views/settings/account/notifications/fields2");
var utils_1 = require("app/views/settings/account/notifications/utils");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var NotificationSettings = /** @class */ (function (_super) {
    tslib_1.__extends(NotificationSettings, _super);
    function NotificationSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getStateToPutForDefault = function (changedData, notificationType) {
            /**
             * Update the current providers' parent-independent notification settings
             * with the new value. If the new value is "never", then also update all
             * parent-specific notification settings to "default". If the previous value
             * was "never", then assume providerList should be "email" only.
             */
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = utils_1.getStateToPutForDefault(notificationType, notificationSettings, changedData, utils_1.getParentIds(notificationType, notificationSettings));
            _this.setState({
                notificationSettings: utils_1.mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        return _this;
    }
    NotificationSettings.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { notificationSettings: {}, legacyData: {} });
    };
    NotificationSettings.prototype.getEndpoints = function () {
        return [
            ['notificationSettings', "/users/me/notification-settings/"],
            ['legacyData', '/users/me/notifications/'],
        ];
    };
    NotificationSettings.prototype.getInitialData = function () {
        var notificationSettings = this.state.notificationSettings;
        return Object.fromEntries(constants_1.NOTIFICATION_SETTINGS_TYPES.map(function (notificationType) { return [
            notificationType,
            utils_1.decideDefault(notificationType, notificationSettings),
        ]; }));
    };
    NotificationSettings.prototype.getFields = function () {
        var _this = this;
        return constants_1.NOTIFICATION_SETTINGS_TYPES.map(function (notificationType) {
            return Object.assign({}, fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType], {
                getData: function (data) { return _this.getStateToPutForDefault(data, notificationType); },
                help: (<react_1.default.Fragment>
              {fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType].help}
              &nbsp;
              <link_1.default to={"/settings/account/notifications/" + notificationType}>
                Fine tune
              </link_1.default>
            </react_1.default.Fragment>),
            });
        });
    };
    NotificationSettings.prototype.renderBody = function () {
        var legacyData = this.state.legacyData;
        return (<react_1.default.Fragment>
        <settingsPageHeader_1.default title="Notifications"/>
        <textBlock_1.default>Personal notifications sent via email or an integration.</textBlock_1.default>
        <feedbackAlert_1.default />
        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={this.getInitialData()}>
          <jsonForm_1.default title={locale_1.t('Notifications')} fields={this.getFields()}/>
        </form_1.default>
        <form_1.default initialData={legacyData} saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/">
          <jsonForm_1.default title={locale_1.t('My Activity')} fields={constants_1.SELF_NOTIFICATION_SETTINGS_TYPES.map(function (type) { return fields2_1.NOTIFICATION_SETTING_FIELDS[type]; })}/>
        </form_1.default>
        <alertLink_1.default to="/settings/account/emails" icon={<icons_1.IconMail />}>
          {locale_1.t('Looking to add or remove an email address? Use the emails panel.')}
        </alertLink_1.default>
      </react_1.default.Fragment>);
    };
    return NotificationSettings;
}(asyncComponent_1.default));
exports.default = NotificationSettings;
//# sourceMappingURL=notificationSettings.jsx.map