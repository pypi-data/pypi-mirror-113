Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var locale_1 = require("app/locale");
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var utils_1 = require("app/views/settings/account/notifications/utils");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var NotificationSettingsByOrganization = /** @class */ (function (_super) {
    tslib_1.__extends(NotificationSettingsByOrganization, _super);
    function NotificationSettingsByOrganization() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NotificationSettingsByOrganization.prototype.render = function () {
        var _a = this.props, notificationType = _a.notificationType, notificationSettings = _a.notificationSettings, onChange = _a.onChange, organizations = _a.organizations;
        return (<form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={utils_1.getParentData(notificationType, notificationSettings, organizations)}>
        <jsonForm_1.default title={locale_1.t('Organizations')} fields={organizations.map(function (organization) {
                return utils_1.getParentField(notificationType, notificationSettings, organization, onChange);
            })}/>
      </form_1.default>);
    };
    return NotificationSettingsByOrganization;
}(react_1.default.Component));
exports.default = withOrganizations_1.default(NotificationSettingsByOrganization);
//# sourceMappingURL=notificationSettingsByOrganization.jsx.map