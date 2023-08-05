Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var modalActions_1 = tslib_1.__importDefault(require("app/actions/modalActions"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var actions_1 = tslib_1.__importDefault(require("app/views/organizationGroupDetails/actions"));
// @ts-expect-error
var group = TestStubs.Group({
    id: '1337',
    pluginActions: [],
    pluginIssues: [],
});
// @ts-expect-error
var project = TestStubs.ProjectDetails({
    id: '2448',
    name: 'project name',
    slug: 'project',
});
// @ts-expect-error
var organization = TestStubs.Organization({
    id: '4660',
    slug: 'org',
    features: ['reprocessing-v2'],
});
function renderComponent(event) {
    return enzyme_1.mountWithTheme(<actions_1.default group={group} project={project} organization={organization} event={event} disabled={false}/>);
}
describe('GroupActions', function () {
    beforeEach(function () {
        jest.spyOn(configStore_1.default, 'get').mockImplementation(function () { return []; });
    });
    describe('render()', function () {
        it('renders correctly', function () {
            var wrapper = renderComponent();
            expect(wrapper).toSnapshot();
        });
    });
    describe('subscribing', function () {
        var issuesApi;
        beforeEach(function () {
            // @ts-expect-error
            issuesApi = MockApiClient.addMockResponse({
                url: '/projects/org/project/issues/',
                method: 'PUT',
                // @ts-expect-error
                body: TestStubs.Group({ isSubscribed: false }),
            });
        });
        it('can subscribe', function () {
            var wrapper = renderComponent();
            var btn = wrapper.find('button[aria-label="Subscribe"]');
            btn.simulate('click');
            expect(issuesApi).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
                data: { isSubscribed: true },
            }));
        });
    });
    describe('bookmarking', function () {
        var issuesApi;
        beforeEach(function () {
            // @ts-expect-error
            issuesApi = MockApiClient.addMockResponse({
                url: '/projects/org/project/issues/',
                method: 'PUT',
                // @ts-expect-error
                body: TestStubs.Group({ isBookmarked: false }),
            });
        });
        it('can bookmark', function () {
            var wrapper = renderComponent();
            var btn = wrapper.find('button[aria-label="Bookmark"]');
            btn.simulate('click');
            expect(issuesApi).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
                data: { isBookmarked: true },
            }));
        });
    });
    describe('reprocessing', function () {
        it('renders ReprocessAction component if org has feature flag reprocessing-v2', function () {
            var wrapper = renderComponent();
            var reprocessActionButton = wrapper.find('ReprocessAction');
            expect(reprocessActionButton).toBeTruthy();
        });
        it('open dialog by clicking on the ReprocessAction component', function () {
            return tslib_1.__awaiter(this, void 0, void 0, function () {
                var event, onReprocessEventFunc, wrapper, reprocessActionButton;
                return tslib_1.__generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            event = TestStubs.EventStacktraceException({
                                platform: 'native',
                            });
                            onReprocessEventFunc = jest.spyOn(modalActions_1.default, 'openModal');
                            wrapper = renderComponent(event);
                            reprocessActionButton = wrapper.find('ReprocessAction');
                            expect(reprocessActionButton).toBeTruthy();
                            reprocessActionButton.simulate('click');
                            // @ts-expect-error
                            return [4 /*yield*/, tick()];
                        case 1:
                            // @ts-expect-error
                            _a.sent();
                            expect(onReprocessEventFunc).toHaveBeenCalled();
                            return [2 /*return*/];
                    }
                });
            });
        });
    });
});
//# sourceMappingURL=actions.spec.jsx.map