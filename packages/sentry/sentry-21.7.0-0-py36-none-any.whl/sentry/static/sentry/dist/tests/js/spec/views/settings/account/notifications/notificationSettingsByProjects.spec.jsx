Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var notificationSettingsByProjects_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettingsByProjects"));
var createWrapper = function (projects) {
    var routerContext = initializeOrg_1.initializeOrg().routerContext;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/projects/',
        method: 'GET',
        body: projects,
    });
    var notificationSettings = {
        alerts: {
            user: { me: { email: 'always', slack: 'always' } },
            project: Object.fromEntries(projects.map(function (project) { return [project.id, { email: 'never', slack: 'never' }]; })),
        },
    };
    return enzyme_1.mountWithTheme(<notificationSettingsByProjects_1.default notificationType="alerts" notificationSettings={notificationSettings} onChange={jest.fn()}/>, routerContext);
};
describe('NotificationSettingsByProjects', function () {
    it('should render when there are no projects', function () {
        var wrapper = createWrapper([]);
        expect(wrapper.find('EmptyMessage').text()).toEqual('No projects found');
        expect(wrapper.find('AsyncComponentSearchInput')).toHaveLength(0);
        expect(wrapper.find('Pagination')).toHaveLength(0);
    });
    it('should show search bar when there are enough projects', function () {
        // @ts-expect-error
        var organization = TestStubs.Organization();
        var projects = tslib_1.__spreadArray([], tslib_1.__read(Array(3).keys())).map(function (id) {
            // @ts-expect-error
            return TestStubs.Project({ organization: organization, id: id });
        });
        var wrapper = createWrapper(projects);
        expect(wrapper.find('AsyncComponentSearchInput')).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByProjects.spec.jsx.map