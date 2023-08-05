Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var locale_1 = require("app/locale");
var feedbackAlert_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/feedbackAlert"));
var fields_1 = require("app/views/settings/account/notifications/fields");
var fields2_1 = require("app/views/settings/account/notifications/fields2");
var notificationSettingsByOrganization_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettingsByOrganization"));
var notificationSettingsByProjects_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettingsByProjects"));
var utils_1 = require("app/views/settings/account/notifications/utils");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var NotificationSettingsByType = /** @class */ (function (_super) {
    tslib_1.__extends(NotificationSettingsByType, _super);
    function NotificationSettingsByType() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /* Methods responsible for updating state and hitting the API. */
        _this.getStateToPutForProvider = function (changedData) {
            var notificationType = _this.props.notificationType;
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = utils_1.getStateToPutForProvider(notificationType, notificationSettings, changedData);
            _this.setState({
                notificationSettings: utils_1.mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        _this.getStateToPutForDefault = function (changedData) {
            var notificationType = _this.props.notificationType;
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = utils_1.getStateToPutForDefault(notificationType, notificationSettings, changedData, utils_1.getParentIds(notificationType, notificationSettings));
            _this.setState({
                notificationSettings: utils_1.mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        _this.getStateToPutForParent = function (changedData, parentId) {
            var notificationType = _this.props.notificationType;
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = utils_1.getStateToPutForParent(notificationType, notificationSettings, changedData, parentId);
            _this.setState({
                notificationSettings: utils_1.mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        return _this;
    }
    NotificationSettingsByType.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { notificationSettings: {} });
    };
    NotificationSettingsByType.prototype.getEndpoints = function () {
        var notificationType = this.props.notificationType;
        var query = { type: notificationType };
        return [['notificationSettings', "/users/me/notification-settings/", { query: query }]];
    };
    /* Methods responsible for rendering the page. */
    NotificationSettingsByType.prototype.getInitialData = function () {
        var _a;
        var notificationType = this.props.notificationType;
        var notificationSettings = this.state.notificationSettings;
        var initialData = (_a = {},
            _a[notificationType] = utils_1.getCurrentDefault(notificationType, notificationSettings),
            _a);
        if (!utils_1.isEverythingDisabled(notificationType, notificationSettings)) {
            initialData.provider = utils_1.providerListToString(utils_1.getCurrentProviders(notificationType, notificationSettings));
        }
        return initialData;
    };
    NotificationSettingsByType.prototype.getFields = function () {
        var _this = this;
        var notificationType = this.props.notificationType;
        var notificationSettings = this.state.notificationSettings;
        var fields = [
            Object.assign({}, fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType], {
                help: locale_1.t('This is the default for all projects.'),
                getData: function (data) { return _this.getStateToPutForDefault(data); },
            }),
        ];
        if (!utils_1.isEverythingDisabled(notificationType, notificationSettings)) {
            fields.push(Object.assign({
                help: locale_1.t('Where personal notifications will be sent.'),
                getData: function (data) { return _this.getStateToPutForProvider(data); },
            }, fields2_1.NOTIFICATION_SETTING_FIELDS.provider));
        }
        return fields;
    };
    NotificationSettingsByType.prototype.renderBody = function () {
        var notificationType = this.props.notificationType;
        var notificationSettings = this.state.notificationSettings;
        var _a = fields_1.ACCOUNT_NOTIFICATION_FIELDS[notificationType], title = _a.title, description = _a.description;
        return (<react_1.default.Fragment>
        <settingsPageHeader_1.default title={title}/>
        {description && <textBlock_1.default>{description}</textBlock_1.default>}
        <feedbackAlert_1.default />
        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={this.getInitialData()}>
          <jsonForm_1.default title={utils_1.isGroupedByProject(notificationType)
                ? locale_1.t('All Projects')
                : locale_1.t('All Organizations')} fields={this.getFields()}/>
        </form_1.default>
        {!utils_1.isEverythingDisabled(notificationType, notificationSettings) &&
                (utils_1.isGroupedByProject(notificationType) ? (<notificationSettingsByProjects_1.default notificationType={notificationType} notificationSettings={notificationSettings} onChange={this.getStateToPutForParent}/>) : (<notificationSettingsByOrganization_1.default notificationType={notificationType} notificationSettings={notificationSettings} onChange={this.getStateToPutForParent}/>))}
      </react_1.default.Fragment>);
    };
    return NotificationSettingsByType;
}(asyncComponent_1.default));
exports.default = NotificationSettingsByType;
//# sourceMappingURL=notificationSettingsByType.jsx.map