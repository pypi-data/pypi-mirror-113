Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var histogram_1 = require("app/utils/performance/histogram");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var utils_1 = require("../../utils");
var filter_1 = require("../filter");
var latencyChart_1 = require("../latencyChart");
var content_1 = tslib_1.__importDefault(require("./content"));
var utils_2 = require("./utils");
var TransactionEvents = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionEvents, _super);
    function TransactionEvents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            spanOperationBreakdownFilter: filter_1.decodeFilterFromLocation(_this.props.location),
            eventsDisplayFilterName: utils_2.decodeEventsDisplayFilterFromLocation(_this.props.location),
            eventView: generateEventsEventView(_this.props.location, utils_1.getTransactionName(_this.props.location)),
        };
        _this.onChangeSpanOperationBreakdownFilter = function (newFilter) {
            var _a;
            var _b = _this.props, location = _b.location, organization = _b.organization;
            var _c = _this.state, spanOperationBreakdownFilter = _c.spanOperationBreakdownFilter, eventsDisplayFilterName = _c.eventsDisplayFilterName, eventView = _c.eventView;
            analytics_1.trackAnalyticsEvent({
                eventName: 'Performance Views: Transaction Events Ops Breakdown Filter Dropdown',
                eventKey: 'performance_views.transactionEvents.ops_filter_dropdown.selection',
                organization_id: parseInt(organization.id, 10),
                action: newFilter,
            });
            // Check to see if the current table sort matches the EventsDisplayFilter.
            // If it does, we can re-sort using the new SpanOperationBreakdownFilter
            var eventsFilterOptionSort = utils_2.getEventsFilterOptions(spanOperationBreakdownFilter)[eventsDisplayFilterName].sort;
            var currentSort = (_a = eventView === null || eventView === void 0 ? void 0 : eventView.sorts) === null || _a === void 0 ? void 0 : _a[0];
            var sortQuery = {};
            if ((eventsFilterOptionSort === null || eventsFilterOptionSort === void 0 ? void 0 : eventsFilterOptionSort.kind) === (currentSort === null || currentSort === void 0 ? void 0 : currentSort.kind) &&
                (eventsFilterOptionSort === null || eventsFilterOptionSort === void 0 ? void 0 : eventsFilterOptionSort.field) === (currentSort === null || currentSort === void 0 ? void 0 : currentSort.field)) {
                sortQuery = utils_2.filterEventsDisplayToLocationQuery(eventsDisplayFilterName, newFilter);
            }
            var nextQuery = tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, histogram_1.removeHistogramQueryStrings(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), filter_1.filterToLocationQuery(newFilter)), sortQuery);
            if (newFilter === filter_1.SpanOperationBreakdownFilter.None) {
                delete nextQuery.breakdown;
            }
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: nextQuery,
            });
        };
        _this.onChangeEventsDisplayFilter = function (newFilterName) {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventName: 'Performance Views: Transaction Events Display Filter Dropdown',
                eventKey: 'performance_views.transactionEvents.display_filter_dropdown.selection',
                organization_id: parseInt(organization.id, 10),
                action: newFilterName,
            });
            _this.filterDropdownSortEvents(newFilterName);
        };
        _this.filterDropdownSortEvents = function (newFilterName) {
            var location = _this.props.location;
            var spanOperationBreakdownFilter = _this.state.spanOperationBreakdownFilter;
            var nextQuery = tslib_1.__assign(tslib_1.__assign({}, histogram_1.removeHistogramQueryStrings(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), utils_2.filterEventsDisplayToLocationQuery(newFilterName, spanOperationBreakdownFilter));
            if (newFilterName === utils_2.EventsDisplayFilterName.p100) {
                delete nextQuery.showTransaction;
            }
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: nextQuery,
            });
        };
        _this.getFilteredEventView = function (percentiles) {
            var _a = _this.state, eventsDisplayFilterName = _a.eventsDisplayFilterName, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, eventView = _a.eventView;
            var filter = utils_2.getEventsFilterOptions(spanOperationBreakdownFilter, percentiles)[eventsDisplayFilterName];
            var filteredEventView = eventView === null || eventView === void 0 ? void 0 : eventView.clone();
            if (filteredEventView && (filter === null || filter === void 0 ? void 0 : filter.query)) {
                var query_1 = tokenizeSearch_1.tokenizeSearch(filteredEventView.query);
                filter.query.forEach(function (item) { return query_1.setTagValues(item[0], [item[1]]); });
                filteredEventView.query = query_1.formatString();
            }
            return filteredEventView;
        };
        _this.renderNoAccess = function () {
            return <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>;
        };
        return _this;
    }
    TransactionEvents.getDerivedStateFromProps = function (nextProps, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { spanOperationBreakdownFilter: filter_1.decodeFilterFromLocation(nextProps.location), eventsDisplayFilterName: utils_2.decodeEventsDisplayFilterFromLocation(nextProps.location), eventView: generateEventsEventView(nextProps.location, utils_1.getTransactionName(nextProps.location)) });
    };
    TransactionEvents.prototype.getDocumentTitle = function () {
        var name = utils_1.getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), locale_1.t('Events')].join(' \u2014 ');
        }
        return [locale_1.t('Summary'), locale_1.t('Events')].join(' \u2014 ');
    };
    TransactionEvents.prototype.getPercentilesEventView = function (eventView) {
        var percentileColumns = [
            {
                kind: 'function',
                function: ['p100', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p99', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p95', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p75', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p50', '', undefined, undefined],
            },
        ];
        return eventView.withColumns(tslib_1.__spreadArray([], tslib_1.__read(percentileColumns)));
    };
    TransactionEvents.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = utils_1.getTransactionName(location);
        var webVital = getWebVital(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            react_router_1.browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: tslib_1.__assign({}, location.query),
            });
            return null;
        }
        var percentilesView = this.getPercentilesEventView(eventView);
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <feature_1.default features={['performance-events-page']} organization={organization} renderDisabled={this.renderNoAccess}>
          <globalSelectionHeader_1.default lockedMessageSubject={locale_1.t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
            <lightWeightNoProjectMessage_1.default organization={organization}>
              <discoverQuery_1.default eventView={percentilesView} orgSlug={organization.slug} location={location} referrer="api.performance.transaction-events">
                {function (_a) {
                var _b;
                var isLoading = _a.isLoading, tableData = _a.tableData;
                var percentiles = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0];
                return (<content_1.default location={location} eventView={_this.getFilteredEventView(percentiles)} transactionName={transactionName} organization={organization} projects={projects} spanOperationBreakdownFilter={_this.state.spanOperationBreakdownFilter} onChangeSpanOperationBreakdownFilter={_this.onChangeSpanOperationBreakdownFilter} eventsDisplayFilterName={_this.state.eventsDisplayFilterName} onChangeEventsDisplayFilter={_this.onChangeEventsDisplayFilter} percentileValues={percentiles} isLoading={isLoading} webVital={webVital}/>);
            }}
              </discoverQuery_1.default>
            </lightWeightNoProjectMessage_1.default>
          </globalSelectionHeader_1.default>
        </feature_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return TransactionEvents;
}(react_1.Component));
function getWebVital(location) {
    var webVital = queryString_1.decodeScalar(location.query.webVital, '');
    if (Object.values(fields_1.WebVital).includes(webVital)) {
        return webVital;
    }
    return undefined;
}
function generateEventsEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    var query = queryString_1.decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (fields_1.isAggregateField(field))
            conditions.removeTag(field);
    });
    // Default fields for relative span view
    var fields = [
        'id',
        'user.display',
        fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
        'transaction.duration',
        'trace',
        'timestamp',
    ];
    var breakdown = filter_1.decodeFilterFromLocation(location);
    if (breakdown !== filter_1.SpanOperationBreakdownFilter.None) {
        fields.splice(2, 1, "spans." + breakdown);
    }
    else {
        fields.push.apply(fields, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields_1.SPAN_OP_BREAKDOWN_FIELDS)), ['spans.total.time']));
    }
    var webVital = getWebVital(location);
    if (webVital) {
        fields.splice(3, 0, webVital);
    }
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: fields,
        query: conditions.formatString(),
        projects: [],
        orderby: queryString_1.decodeScalar(location.query.sort, '-timestamp'),
    }, location);
}
exports.default = withGlobalSelection_1.default(withProjects_1.default(withOrganization_1.default(TransactionEvents)));
//# sourceMappingURL=index.jsx.map