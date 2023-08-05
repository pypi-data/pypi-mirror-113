Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var notificationSettingsByOrganization_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettingsByOrganization"));
var createWrapper = function (notificationSettings) {
    var _a = initializeOrg_1.initializeOrg(), organization = _a.organization, routerContext = _a.routerContext;
    return enzyme_1.mountWithTheme(<notificationSettingsByOrganization_1.default notificationType="alerts" notificationSettings={notificationSettings} organizations={[organization]} onChange={jest.fn()}/>, routerContext);
};
describe('NotificationSettingsByOrganization', function () {
    it('should render', function () {
        var wrapper = createWrapper({
            alerts: {
                user: { me: { email: 'always', slack: 'always' } },
                organization: { 1: { email: 'always', slack: 'always' } },
            },
        });
        expect(wrapper.find('Select')).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByOrganizations.spec.jsx.map