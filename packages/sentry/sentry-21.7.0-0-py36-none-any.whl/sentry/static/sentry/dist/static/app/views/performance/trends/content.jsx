Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var constants_1 = require("app/constants");
var iconFlag_1 = require("app/icons/iconFlag");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var utils_1 = require("../utils");
var changedTransactions_1 = tslib_1.__importDefault(require("./changedTransactions"));
var types_1 = require("./types");
var utils_2 = require("./utils");
var TrendsContent = /** @class */ (function (_super) {
    tslib_1.__extends(TrendsContent, _super);
    function TrendsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleSearch = function (searchQuery) {
            var location = _this.props.location;
            var cursors = utils_2.resetCursors();
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, location.query), cursors), { query: String(searchQuery).trim() || undefined }),
            });
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        _this.handleTrendFunctionChange = function (field) {
            var _a = _this.props, organization = _a.organization, location = _a.location;
            var offsets = {};
            Object.values(types_1.TrendChangeType).forEach(function (trendChangeType) {
                var queryKey = utils_2.getSelectedQueryKey(trendChangeType);
                offsets[queryKey] = undefined;
            });
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.trends.change_function',
                eventName: 'Performance Views: Change Function',
                organization_id: parseInt(organization.id, 10),
                function_name: field,
            });
            _this.setState({
                previousTrendFunction: utils_2.getCurrentTrendFunction(location).field,
            });
            var cursors = utils_2.resetCursors();
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, location.query), offsets), cursors), { trendFunction: field }),
            });
        };
        _this.handleParameterChange = function (label) {
            var _a = _this.props, organization = _a.organization, location = _a.location;
            var cursors = utils_2.resetCursors();
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.trends.change_parameter',
                eventName: 'Performance Views: Change Parameter',
                organization_id: parseInt(organization.id, 10),
                parameter_name: label,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, location.query), cursors), { trendParameter: label }),
            });
        };
        return _this;
    }
    TrendsContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<iconFlag_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    };
    TrendsContent.prototype.getPerformanceLink = function () {
        var location = this.props.location;
        var newQuery = tslib_1.__assign({}, location.query);
        var query = queryString_1.decodeScalar(location.query.query, '');
        var conditions = tokenizeSearch_1.tokenizeSearch(query);
        // This stops errors from occurring when navigating to other views since we are appending aggregates to the trends view
        conditions.removeTag('tpm()');
        conditions.removeTag('confidence()');
        conditions.removeTag('transaction.duration');
        newQuery.query = conditions.formatString();
        return {
            pathname: utils_1.getPerformanceLandingUrl(this.props.organization),
            query: newQuery,
        };
    };
    TrendsContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, eventView = _a.eventView, location = _a.location;
        var previousTrendFunction = this.state.previousTrendFunction;
        var trendView = eventView.clone();
        utils_2.modifyTrendsViewDefaultPeriod(trendView, location);
        var fields = fields_1.generateAggregateFields(organization, [
            {
                field: 'absolute_correlation()',
            },
            {
                field: 'trend_percentage()',
            },
            {
                field: 'trend_difference()',
            },
            {
                field: 'count_percentage()',
            },
            {
                field: 'tpm()',
            },
            {
                field: 'tps()',
            },
        ], ['epm()', 'eps()']);
        var currentTrendFunction = utils_2.getCurrentTrendFunction(location);
        var currentTrendParameter = utils_2.getCurrentTrendParameter(location);
        var query = utils_1.getTransactionSearchQuery(location);
        var TRENDS_PARAMETERS = utils_2.getTrendsParameters({
            canSeeSpanOpTrends: organization.features.includes('performance-ops-breakdown'),
        });
        return (<globalSelectionHeader_1.default defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: utils_2.DEFAULT_TRENDS_STATS_PERIOD,
                },
            }}>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumbs_1.default crumbs={[
                {
                    label: 'Performance',
                    to: this.getPerformanceLink(),
                },
                {
                    label: 'Trends',
                },
            ]}/>
            <Layout.Title>{locale_1.t('Trends')}</Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>
            <DefaultTrends location={location} eventView={eventView}>
              <StyledSearchContainer>
                <StyledSearchBar searchSource="trends" organization={organization} projectIds={trendView.project} query={query} fields={fields} onSearch={this.handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
                <TrendsDropdown>
                  <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Percentile') }} label={currentTrendFunction.label}>
                    {utils_2.TRENDS_FUNCTIONS.map(function (_a) {
                var label = _a.label, field = _a.field;
                return (<dropdownControl_1.DropdownItem key={field} onSelect={_this.handleTrendFunctionChange} eventKey={field} data-test-id={field} isActive={field === currentTrendFunction.field}>
                        {label}
                      </dropdownControl_1.DropdownItem>);
            })}
                  </dropdownControl_1.default>
                </TrendsDropdown>
                <TrendsDropdown>
                  <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Parameter') }} label={currentTrendParameter.label}>
                    {TRENDS_PARAMETERS.map(function (_a) {
                var label = _a.label;
                return (<dropdownControl_1.DropdownItem key={label} onSelect={_this.handleParameterChange} eventKey={label} data-test-id={label} isActive={label === currentTrendParameter.label}>
                        {label}
                      </dropdownControl_1.DropdownItem>);
            })}
                  </dropdownControl_1.default>
                </TrendsDropdown>
              </StyledSearchContainer>
              <TrendsLayoutContainer>
                <changedTransactions_1.default trendChangeType={types_1.TrendChangeType.IMPROVED} previousTrendFunction={previousTrendFunction} trendView={trendView} location={location} setError={this.setError}/>
                <changedTransactions_1.default trendChangeType={types_1.TrendChangeType.REGRESSION} previousTrendFunction={previousTrendFunction} trendView={trendView} location={location} setError={this.setError}/>
              </TrendsLayoutContainer>
            </DefaultTrends>
          </Layout.Main>
        </Layout.Body>
      </globalSelectionHeader_1.default>);
    };
    return TrendsContent;
}(React.Component));
var DefaultTrends = /** @class */ (function (_super) {
    tslib_1.__extends(DefaultTrends, _super);
    function DefaultTrends() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasPushedDefaults = false;
        return _this;
    }
    DefaultTrends.prototype.render = function () {
        var _a = this.props, children = _a.children, location = _a.location, eventView = _a.eventView;
        var queryString = queryString_1.decodeScalar(location.query.query);
        var trendParameter = utils_2.getCurrentTrendParameter(location);
        var conditions = tokenizeSearch_1.tokenizeSearch(queryString || '');
        if (queryString || this.hasPushedDefaults) {
            this.hasPushedDefaults = true;
            return <React.Fragment>{children}</React.Fragment>;
        }
        else {
            this.hasPushedDefaults = true;
            conditions.setTagValues('tpm()', ['>0.01']);
            conditions.setTagValues(trendParameter.column, ['>0', "<" + utils_2.DEFAULT_MAX_DURATION]);
        }
        var query = conditions.formatString();
        eventView.query = query;
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: String(query).trim() || undefined }),
        });
        return null;
    };
    return DefaultTrends;
}(React.Component));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"], ["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var TrendsDropdown = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  flex-grow: 0;\n"], ["\n  margin-left: ", ";\n  flex-grow: 0;\n"])), space_1.default(1));
var StyledSearchContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var TrendsLayoutContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(0, 1fr));\n    align-items: stretch;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(0, 1fr));\n    align-items: stretch;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[1]; });
exports.default = withGlobalSelection_1.default(TrendsContent);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=content.jsx.map