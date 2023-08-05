Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var notificationSettings_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettings"));
var createWrapper = function (notificationSettings) {
    var routerContext = initializeOrg_1.initializeOrg().routerContext;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notification-settings/',
        method: 'GET',
        body: notificationSettings,
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notifications/',
        method: 'GET',
        body: {
            personalActivityNotifications: true,
            selfAssignOnResolve: true,
            weeklyReports: true,
        },
    });
    return enzyme_1.mountWithTheme(<notificationSettings_1.default />, routerContext);
};
describe('NotificationSettings', function () {
    it('should render', function () {
        var wrapper = createWrapper({
            alerts: { user: { me: { email: 'never', slack: 'never' } } },
            deploy: { user: { me: { email: 'never', slack: 'never' } } },
            workflow: { user: { me: { email: 'never', slack: 'never' } } },
        });
        // There are 7 notification setting Selects/Toggles.
        var fields = wrapper.find('Field');
        expect(fields).toHaveLength(7);
    });
});
//# sourceMappingURL=notificationSettings.spec.jsx.map