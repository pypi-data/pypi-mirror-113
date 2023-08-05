Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var locale_1 = require("app/locale");
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var filter_1 = require("app/views/performance/transactionSummary/filter");
var content_1 = tslib_1.__importDefault(require("app/views/performance/transactionSummary/transactionEvents/content"));
var utils_1 = require("app/views/performance/transactionSummary/transactionEvents/utils");
function initializeData(_a) {
    var _b = _a.features, additionalFeatures = _b === void 0 ? [] : _b;
    var features = tslib_1.__spreadArray(['discover-basic', 'performance-view'], tslib_1.__read(additionalFeatures));
    // @ts-expect-error
    var organization = TestStubs.Organization({
        features: features,
        // @ts-expect-error
        projects: [TestStubs.Project()],
        apdexThreshold: 400,
    });
    var initialData = initializeOrg_1.initializeOrg({
        organization: organization,
        router: {
            location: {
                query: {
                    transaction: '/performance',
                    project: 1,
                    transactionCursor: '1:0:0',
                },
            },
        },
        project: 1,
        projects: [],
    });
    projectsStore_1.default.loadInitialData(initialData.organization.projects);
    return initialData;
}
describe('Performance Transaction Events Content', function () {
    var fields;
    var organization;
    var data;
    var transactionName;
    var eventView;
    var initialData;
    var query = 'transaction.duration:<15m event.type:transaction transaction:/api/0/organizations/{organization_slug}/eventsv2/';
    beforeEach(function () {
        transactionName = 'transactionName';
        fields = tslib_1.__spreadArray([
            'id',
            'user.display',
            fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
            'transaction.duration',
            'trace',
            'timestamp',
            'spans.total.time'
        ], tslib_1.__read(fields_1.SPAN_OP_BREAKDOWN_FIELDS));
        // @ts-expect-error
        organization = TestStubs.Organization();
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/projects/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/is-key-transactions/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/prompts-activity/',
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: "/organizations/org-slug/legacy-key-transactions-count/",
            body: [],
        });
        data = [
            {
                id: 'deadbeef',
                'user.display': 'uhoh@example.com',
                'transaction.duration': 400,
                'project.id': 1,
                timestamp: '2020-05-21T15:31:18+00:00',
                trace: '1234',
                'span_ops_breakdown.relative': '',
                'spans.browser': 100,
                'spans.db': 30,
                'spans.http': 170,
                'spans.resource': 100,
                'spans.total.time': 400,
            },
            {
                id: 'moredeadbeef',
                'user.display': 'moreuhoh@example.com',
                'transaction.duration': 600,
                'project.id': 1,
                timestamp: '2020-05-22T15:31:18+00:00',
                trace: '4321',
                'span_ops_breakdown.relative': '',
                'spans.browser': 100,
                'spans.db': 300,
                'spans.http': 100,
                'spans.resource': 100,
                'spans.total.time': 600,
            },
        ];
        // Transaction list response
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/eventsv2/',
            headers: {
                Link: '<http://localhost/api/0/organizations/org-slug/eventsv2/?cursor=2:0:0>; rel="next"; results="true"; cursor="2:0:0",' +
                    '<http://localhost/api/0/organizations/org-slug/eventsv2/?cursor=1:0:0>; rel="previous"; results="false"; cursor="1:0:0"',
            },
            body: {
                meta: {
                    id: 'string',
                    'user.display': 'string',
                    'transaction.duration': 'duration',
                    'project.id': 'integer',
                    timestamp: 'date',
                },
                data: data,
            },
        }, {
            predicate: function (url, options) {
                var _a;
                return (url.includes('eventsv2') && ((_a = options.query) === null || _a === void 0 ? void 0 : _a.field.includes('user.display')));
            },
        });
        initialData = initializeData({ features: ['performance-events-page'] });
        eventView = eventView_1.default.fromNewQueryWithLocation({
            id: undefined,
            version: 2,
            name: 'transactionName',
            fields: fields,
            query: query,
            projects: [],
            orderby: '-timestamp',
        }, initialData.router.location);
    });
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
        projectsStore_1.default.reset();
        jest.clearAllMocks();
    });
    it('basic rendering', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var wrapper, columnTitles;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        wrapper = enzyme_1.mountWithTheme(<content_1.default eventView={eventView} organization={organization} location={initialData.router.location} transactionName={transactionName} projects={initialData.projects} spanOperationBreakdownFilter={filter_1.SpanOperationBreakdownFilter.None} onChangeSpanOperationBreakdownFilter={function () { }} eventsDisplayFilterName={utils_1.EventsDisplayFilterName.p100} onChangeEventsDisplayFilter={function () { }} isLoading={false}/>, initialData.routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _a.sent();
                        wrapper.update();
                        expect(wrapper.find('EventsTable')).toHaveLength(1);
                        expect(wrapper.find('SearchRowMenuItem')).toHaveLength(2);
                        expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
                        expect(wrapper.find('Filter')).toHaveLength(1);
                        expect(wrapper.find('TransactionHeader')).toHaveLength(1);
                        columnTitles = wrapper.find('EventsTable').props().columnTitles;
                        expect(columnTitles).toEqual([
                            locale_1.t('event id'),
                            locale_1.t('user'),
                            locale_1.t('operation duration'),
                            locale_1.t('total duration'),
                            locale_1.t('trace id'),
                            locale_1.t('timestamp'),
                        ]);
                        return [2 /*return*/];
                }
            });
        });
    });
    it('rendering with webvital selected', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var wrapper, columnTitles;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        wrapper = enzyme_1.mountWithTheme(<content_1.default eventView={eventView} organization={organization} location={initialData.router.location} transactionName={transactionName} projects={initialData.projects} spanOperationBreakdownFilter={filter_1.SpanOperationBreakdownFilter.None} onChangeSpanOperationBreakdownFilter={function () { }} eventsDisplayFilterName={utils_1.EventsDisplayFilterName.p100} onChangeEventsDisplayFilter={function () { }} isLoading={false} webVital={fields_1.WebVital.LCP}/>, initialData.routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _a.sent();
                        wrapper.update();
                        expect(wrapper.find('EventsTable')).toHaveLength(1);
                        expect(wrapper.find('SearchRowMenuItem')).toHaveLength(2);
                        expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
                        expect(wrapper.find('Filter')).toHaveLength(1);
                        expect(wrapper.find('TransactionHeader')).toHaveLength(1);
                        columnTitles = wrapper.find('EventsTable').props().columnTitles;
                        expect(columnTitles).toEqual([
                            locale_1.t('event id'),
                            locale_1.t('user'),
                            locale_1.t('operation duration'),
                            locale_1.t('measurements.lcp'),
                            locale_1.t('total duration'),
                            locale_1.t('trace id'),
                            locale_1.t('timestamp'),
                        ]);
                        return [2 /*return*/];
                }
            });
        });
    });
});
//# sourceMappingURL=content.spec.jsx.map