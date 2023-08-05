Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var notificationSettingsByType_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettingsByType"));
var createWrapper = function (notificationSettings) {
    var routerContext = initializeOrg_1.initializeOrg().routerContext;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notification-settings/',
        method: 'GET',
        body: notificationSettings,
    });
    return enzyme_1.mountWithTheme(<notificationSettingsByType_1.default notificationType="alerts"/>, routerContext);
};
describe('NotificationSettingsByType', function () {
    it('should render when everything is disabled', function () {
        var wrapper = createWrapper({
            alerts: { user: { me: { email: 'never', slack: 'never' } } },
        });
        // There is only one field and it is the default and it is set to "off".
        var fields = wrapper.find('Field');
        expect(fields).toHaveLength(1);
        expect(fields.at(0).find('FieldLabel').text()).toEqual('Issue Alerts');
        expect(fields.at(0).find('Select').text()).toEqual('Off');
    });
});
//# sourceMappingURL=notificationSettingsByType.spec.jsx.map