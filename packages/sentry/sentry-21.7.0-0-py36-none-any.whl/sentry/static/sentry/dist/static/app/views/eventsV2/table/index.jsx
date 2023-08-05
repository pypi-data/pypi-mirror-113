Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = require("app/utils/discover/eventView");
var measurements_1 = tslib_1.__importDefault(require("app/utils/measurements/measurements"));
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var constants_1 = require("app/utils/performance/spanOperationBreakdowns/constants");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withTags_1 = tslib_1.__importDefault(require("app/utils/withTags"));
var tableView_1 = tslib_1.__importDefault(require("./tableView"));
/**
 * `Table` is a container element that handles 2 things
 * 1. Fetch data from source
 * 2. Handle pagination of data
 *
 * It will pass the data it fetched to `TableView`, where the state of the
 * Table is maintained and controlled
 */
var Table = /** @class */ (function (_super) {
    tslib_1.__extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            pageLinks: null,
            tableData: null,
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getEventsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return !eventView_1.isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
        };
        _this.fetchData = function () {
            var _a = _this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, setError = _a.setError, confirmedQuery = _a.confirmedQuery;
            if (!eventView.isValid() || !confirmedQuery) {
                return;
            }
            // note: If the eventView has no aggregates, the endpoint will automatically add the event id in
            // the API payload response
            var url = "/organizations/" + organization.slug + "/eventsv2/";
            var tableFetchID = Symbol('tableFetchID');
            var apiPayload = eventView.getEventsAPIPayload(location);
            apiPayload.referrer = 'api.discover.query-table';
            setError('', 200);
            _this.setState({ isLoading: true, tableFetchID: tableFetchID });
            analytics_1.metric.mark({ name: "discover-events-start-" + apiPayload.query });
            _this.props.api.clear();
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: apiPayload,
            })
                .then(function (_a) {
                var _b = tslib_1.__read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
                // We want to measure this metric regardless of whether we use the result
                analytics_1.metric.measure({
                    name: 'app.api.discover-query',
                    start: "discover-events-start-" + apiPayload.query,
                    data: {
                        status: jqXHR && jqXHR.status,
                    },
                });
                if (_this.state.tableFetchID !== tableFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState(function (prevState) { return ({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: null,
                    pageLinks: jqXHR ? jqXHR.getResponseHeader('Link') : prevState.pageLinks,
                    tableData: data,
                }); });
            })
                .catch(function (err) {
                var _a;
                analytics_1.metric.measure({
                    name: 'app.api.discover-query',
                    start: "discover-events-start-" + apiPayload.query,
                    data: {
                        status: err.status,
                    },
                });
                var message = ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || locale_1.t('An unknown error occurred.');
                _this.setState({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: message,
                    pageLinks: null,
                    tableData: null,
                });
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'discover_search.failed',
                    eventName: 'Discover Search: Failed',
                    organization_id: _this.props.organization.id,
                    search_type: 'events',
                    search_source: 'discover_search',
                    error: message,
                });
                setError(message, err.status);
            });
        };
        return _this;
    }
    Table.prototype.componentDidMount = function () {
        this.fetchData();
    };
    Table.prototype.componentDidUpdate = function (prevProps) {
        // Reload data if we aren't already loading, or if we've moved
        // from an invalid view state to a valid one.
        if ((!this.state.isLoading && this.shouldRefetchData(prevProps)) ||
            (prevProps.eventView.isValid() === false && this.props.eventView.isValid()) ||
            prevProps.confirmedQuery !== this.props.confirmedQuery) {
            this.fetchData();
        }
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, tags = _a.tags;
        var _b = this.state, pageLinks = _b.pageLinks, tableData = _b.tableData, isLoading = _b.isLoading, error = _b.error;
        var tagKeys = Object.values(tags).map(function (_a) {
            var key = _a.key;
            return key;
        });
        var isFirstPage = pageLinks
            ? parseLinkHeader_1.default(pageLinks).previous.results === false
            : false;
        return (<Container>
        <measurements_1.default organization={organization}>
          {function (_a) {
                var measurements = _a.measurements;
                var measurementKeys = Object.values(measurements).map(function (_a) {
                    var key = _a.key;
                    return key;
                });
                return (<tableView_1.default {..._this.props} isLoading={isLoading} isFirstPage={isFirstPage} error={error} eventView={eventView} tableData={tableData} tagKeys={tagKeys} measurementKeys={measurementKeys} spanOperationBreakdownKeys={constants_1.SPAN_OP_BREAKDOWN_FIELDS}/>);
            }}
        </measurements_1.default>
        <pagination_1.default pageLinks={pageLinks}/>
      </Container>);
    };
    return Table;
}(react_1.PureComponent));
exports.default = withApi_1.default(withTags_1.default(Table));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  min-width: 0;\n"], ["\n  min-width: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map