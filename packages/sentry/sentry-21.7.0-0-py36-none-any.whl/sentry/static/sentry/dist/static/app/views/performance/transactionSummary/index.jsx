Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var tags_1 = require("app/actionCreators/tags");
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var analytics_1 = require("app/utils/analytics");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var histogram_1 = require("app/utils/performance/histogram");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var utils_1 = require("../utils");
var constants_1 = require("./transactionVitals/constants");
var content_1 = tslib_1.__importDefault(require("./content"));
var filter_1 = require("./filter");
var latencyChart_1 = require("./latencyChart");
var TransactionSummary = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionSummary, _super);
    function TransactionSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
            spanOperationBreakdownFilter: filter_1.decodeFilterFromLocation(_this.props.location),
            eventView: generateSummaryEventView(_this.props.location, utils_1.getTransactionName(_this.props.location)),
        };
        _this.onChangeFilter = function (newFilter) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            analytics_1.trackAnalyticsEvent({
                eventName: 'Performance Views: Filter Dropdown',
                eventKey: 'performance_views.filter_dropdown.selection',
                organization_id: parseInt(organization.id, 10),
                action: newFilter,
            });
            var nextQuery = tslib_1.__assign(tslib_1.__assign({}, histogram_1.removeHistogramQueryStrings(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), filter_1.filterToLocationQuery(newFilter));
            if (newFilter === filter_1.SpanOperationBreakdownFilter.None) {
                delete nextQuery.breakdown;
            }
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: nextQuery,
            });
        };
        return _this;
    }
    TransactionSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { spanOperationBreakdownFilter: filter_1.decodeFilterFromLocation(nextProps.location), eventView: generateSummaryEventView(nextProps.location, utils_1.getTransactionName(nextProps.location)) });
    };
    TransactionSummary.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        tags_1.loadOrganizationTags(api, organization.slug, selection);
        utils_1.addRoutePerformanceContext(selection);
    };
    TransactionSummary.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual_1.default(prevProps.selection.projects, selection.projects) ||
            !isEqual_1.default(prevProps.selection.datetime, selection.datetime)) {
            tags_1.loadOrganizationTags(api, organization.slug, selection);
            utils_1.addRoutePerformanceContext(selection);
        }
    };
    TransactionSummary.prototype.getDocumentTitle = function () {
        var name = utils_1.getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), locale_1.t('Performance')].join(' - ');
        }
        return [locale_1.t('Summary'), locale_1.t('Performance')].join(' - ');
    };
    TransactionSummary.prototype.getTotalsEventView = function (organization, eventView) {
        var threshold = organization.apdexThreshold.toString();
        var vitals = constants_1.VITAL_GROUPS.map(function (_a) {
            var vs = _a.vitals;
            return vs;
        }).reduce(function (keys, vs) {
            vs.forEach(function (vital) { return keys.push(vital); });
            return keys;
        }, []);
        var totalsColumns = [
            {
                kind: 'function',
                function: ['p95', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['count', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['count_unique', 'user', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['failure_rate', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['tpm', '', undefined, undefined],
            },
        ];
        var featureColumns = organization.features.includes('project-transaction-threshold')
            ? [
                {
                    kind: 'function',
                    function: ['count_miserable', 'user', undefined, undefined],
                },
                {
                    kind: 'function',
                    function: ['user_misery', '', undefined, undefined],
                },
                {
                    kind: 'function',
                    function: ['apdex', '', undefined, undefined],
                },
            ]
            : [
                {
                    kind: 'function',
                    function: ['count_miserable', 'user', threshold, undefined],
                },
                {
                    kind: 'function',
                    function: ['user_misery', threshold, undefined, undefined],
                },
                {
                    kind: 'function',
                    function: ['apdex', threshold, undefined, undefined],
                },
            ];
        return eventView.withColumns(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(totalsColumns)), tslib_1.__read(featureColumns)), tslib_1.__read(vitals.map(function (vital) {
            return ({
                kind: 'function',
                function: ['percentile', vital, constants_1.PERCENTILE.toString(), undefined],
            });
        }))));
    };
    TransactionSummary.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var _b = this.state, eventView = _b.eventView, transactionThreshold = _b.transactionThreshold, transactionThresholdMetric = _b.transactionThresholdMetric;
        var transactionName = utils_1.getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            react_router_1.browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: tslib_1.__assign({}, location.query),
            });
            return null;
        }
        var totalsView = this.getTotalsEventView(organization, eventView);
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <globalSelectionHeader_1.default lockedMessageSubject={locale_1.t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
          <StyledPageContent>
            <lightWeightNoProjectMessage_1.default organization={organization}>
              <discoverQuery_1.default eventView={totalsView} orgSlug={organization.slug} location={location} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} referrer="api.performance.transaction-summary">
                {function (_a) {
                var _b, _c;
                var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
                var totals = (_c = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : null;
                return (<content_1.default location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={isLoading} error={error} totalValues={totals} onChangeFilter={_this.onChangeFilter} spanOperationBreakdownFilter={_this.state.spanOperationBreakdownFilter} onChangeThreshold={function (threshold, metric) {
                        return _this.setState({
                            transactionThreshold: threshold,
                            transactionThresholdMetric: metric,
                        });
                    }}/>);
            }}
              </discoverQuery_1.default>
            </lightWeightNoProjectMessage_1.default>
          </StyledPageContent>
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return TransactionSummary;
}(react_1.Component));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function generateSummaryEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    var query = queryString_1.decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (fields_1.isAggregateField(field))
            conditions.removeTag(field);
    });
    var fields = ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp'];
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: fields,
        query: conditions.formatString(),
        projects: [],
    }, location);
}
exports.default = withApi_1.default(withGlobalSelection_1.default(withProjects_1.default(withOrganization_1.default(TransactionSummary))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map