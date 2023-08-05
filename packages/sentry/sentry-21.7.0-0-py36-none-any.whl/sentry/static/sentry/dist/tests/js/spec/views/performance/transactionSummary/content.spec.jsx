Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var content_1 = tslib_1.__importDefault(require("app/views/performance/transactionSummary/content"));
var filter_1 = require("app/views/performance/transactionSummary/filter");
function initialize(projects, query, additionalFeatures) {
    if (additionalFeatures === void 0) { additionalFeatures = []; }
    var features = tslib_1.__spreadArray(['transaction-event', 'performance-view'], tslib_1.__read(additionalFeatures));
    // @ts-expect-error
    var organization = TestStubs.Organization({
        features: features,
        projects: projects,
    });
    var initialOrgData = {
        organization: organization,
        router: {
            location: {
                query: tslib_1.__assign({}, query),
            },
        },
        project: 1,
        projects: [],
    };
    var initialData = initializeOrg_1.initializeOrg(initialOrgData);
    var eventView = eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: 'test-transaction',
        fields: ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp'],
        projects: [],
    }, initialData.router.location);
    var spanOperationBreakdownFilter = filter_1.SpanOperationBreakdownFilter.None;
    var transactionName = 'example-transaction';
    return tslib_1.__assign(tslib_1.__assign({}, initialData), { spanOperationBreakdownFilter: spanOperationBreakdownFilter, transactionName: transactionName, location: initialData.router.location, eventView: eventView });
}
describe('Transaction Summary Content', function () {
    beforeEach(function () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: '/prompts-activity/',
            body: {},
        });
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/sdk-updates/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/eventsv2/',
        body: { data: [{ 'event.type': 'error' }], meta: { 'event.type': 'string' } },
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/users/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/issues/?limit=5&query=is%3Aunresolved%20transaction%3Aexample-transaction&sort=new&statsPeriod=14d',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/events-facets/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/releases/stats/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/events-stats/',
        body: [],
    });
    it('Basic Rendering', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var projects, _a, organization, location, eventView, spanOperationBreakdownFilter, transactionName, routerContext, wrapper, transactionListProps;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        projects = [TestStubs.Project()];
                        _a = initialize(projects, {}), organization = _a.organization, location = _a.location, eventView = _a.eventView, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, transactionName = _a.transactionName;
                        routerContext = TestStubs.routerContext([{ organization: organization }]);
                        wrapper = enzyme_1.mountWithTheme(<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={function () { }}/>, routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('TransactionHeader')).toHaveLength(1);
                        expect(wrapper.find('Filter')).toHaveLength(1);
                        expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
                        expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
                        expect(wrapper.find('TransactionsList')).toHaveLength(1);
                        expect(wrapper.find('UserStats')).toHaveLength(1);
                        expect(wrapper.find('StatusBreakdown')).toHaveLength(1);
                        expect(wrapper.find('SidebarCharts')).toHaveLength(1);
                        expect(wrapper.find('DiscoverQuery')).toHaveLength(2);
                        transactionListProps = wrapper.find('TransactionsList').first().props();
                        expect(transactionListProps.generateDiscoverEventView).toBeDefined();
                        expect(transactionListProps.handleOpenInDiscoverClick).toBeDefined();
                        expect(transactionListProps.generatePerformanceTransactionEventsView).toBeUndefined();
                        expect(transactionListProps.handleOpenAllEventsClick).toBeUndefined();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('Renders with generatePerformanceTransactionEventsView instead when feature flagged', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var projects, _a, organization, location, eventView, spanOperationBreakdownFilter, transactionName, routerContext, wrapper, transactionListProps;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        projects = [TestStubs.Project()];
                        _a = initialize(projects, {}, ['performance-events-page']), organization = _a.organization, location = _a.location, eventView = _a.eventView, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, transactionName = _a.transactionName;
                        routerContext = TestStubs.routerContext([{ organization: organization }]);
                        wrapper = enzyme_1.mountWithTheme(<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={function () { }}/>, routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('TransactionHeader')).toHaveLength(1);
                        expect(wrapper.find('Filter')).toHaveLength(1);
                        expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
                        expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
                        expect(wrapper.find('TransactionsList')).toHaveLength(1);
                        expect(wrapper.find('UserStats')).toHaveLength(1);
                        expect(wrapper.find('StatusBreakdown')).toHaveLength(1);
                        expect(wrapper.find('SidebarCharts')).toHaveLength(1);
                        expect(wrapper.find('DiscoverQuery')).toHaveLength(2);
                        transactionListProps = wrapper.find('TransactionsList').first().props();
                        expect(transactionListProps.generateDiscoverEventView).toBeUndefined();
                        expect(transactionListProps.handleOpenInDiscoverClick).toBeUndefined();
                        expect(transactionListProps.generatePerformanceTransactionEventsView).toBeDefined();
                        expect(transactionListProps.handleOpenAllEventsClick).toBeDefined();
                        return [2 /*return*/];
                }
            });
        });
    });
});
//# sourceMappingURL=content.spec.jsx.map