Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var globalSdkUpdateAlert_1 = tslib_1.__importDefault(require("app/components/globalSdkUpdateAlert"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var cellAction_1 = require("app/views/eventsV2/table/cellAction");
var utils_1 = require("../../landing/utils");
var filter_1 = tslib_1.__importStar(require("../filter"));
var header_1 = tslib_1.__importStar(require("../header"));
var eventsTable_1 = tslib_1.__importDefault(require("./eventsTable"));
var utils_2 = require("./utils");
var EventsPageContent = /** @class */ (function (_super) {
    tslib_1.__extends(EventsPageContent, _super);
    function EventsPageContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
            error: undefined,
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location;
                var searchConditions = tokenizeSearch_1.tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeTag('transaction');
                cellAction_1.updateQuery(searchConditions, action, column, value);
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        return _this;
    }
    EventsPageContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<StyledAlert type="error" icon={<icons_1.IconFlag size="md"/>}>
        {error}
      </StyledAlert>);
    };
    EventsPageContent.prototype.render = function () {
        var _a = this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization, projects = _a.projects, transactionName = _a.transactionName, isLoading = _a.isLoading;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        return (<react_1.Fragment>
        <header_1.default eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={header_1.Tab.Events} hasWebVitals={utils_1.getCurrentLandingDisplay(location, projects, eventView).field ===
                utils_1.LandingDisplayField.FRONTEND_PAGELOAD} handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Layout.Body>
          <StyledSdkUpdatesAlert />
          {this.renderError()}
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            {isLoading ? (<loadingIndicator_1.default />) : (<Body {...this.props} setError={this.setError}/>)}
          </Layout.Main>
        </Layout.Body>
      </react_1.Fragment>);
    };
    return EventsPageContent;
}(React.Component));
var Body = /** @class */ (function (_super) {
    tslib_1.__extends(Body, _super);
    function Body() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Body.prototype.render = function () {
        var eventView = this.props.eventView;
        var _a = this.props, location = _a.location, organization = _a.organization, transactionName = _a.transactionName, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, eventsDisplayFilterName = _a.eventsDisplayFilterName, onChangeEventsDisplayFilter = _a.onChangeEventsDisplayFilter, setError = _a.setError, webVital = _a.webVital;
        var transactionsListTitles = [
            locale_1.t('event id'),
            locale_1.t('user'),
            locale_1.t('operation duration'),
            locale_1.t('total duration'),
            locale_1.t('trace id'),
            locale_1.t('timestamp'),
        ];
        if (webVital) {
            transactionsListTitles.splice(3, 0, locale_1.t(webVital));
        }
        var spanOperationBreakdownConditions = filter_1.filterToSearchConditions(spanOperationBreakdownFilter, location);
        if (spanOperationBreakdownConditions) {
            eventView = eventView.clone();
            eventView.query = (eventView.query + " " + spanOperationBreakdownConditions).trim();
            transactionsListTitles.splice(2, 1, locale_1.t(spanOperationBreakdownFilter + " duration"));
        }
        return (<React.Fragment>
        <Search {...this.props} onChangeEventsDisplayFilter={onChangeEventsDisplayFilter} eventsDisplayFilterName={eventsDisplayFilterName}/>
        <StyledTable>
          <eventsTable_1.default eventView={eventView} organization={organization} location={location} setError={setError} columnTitles={transactionsListTitles} transactionName={transactionName}/>
        </StyledTable>
      </React.Fragment>);
    };
    return Body;
}(React.Component));
var Search = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, spanOperationBreakdownFilter = props.spanOperationBreakdownFilter, onChangeSpanOperationBreakdownFilter = props.onChangeSpanOperationBreakdownFilter, eventsDisplayFilterName = props.eventsDisplayFilterName, onChangeEventsDisplayFilter = props.onChangeEventsDisplayFilter, percentileValues = props.percentileValues;
    var handleSearch = function (query) {
        var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query }));
        // do not propagate pagination when making a new search
        var searchQueryParams = omit_1.default(queryParams, 'cursor');
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: searchQueryParams,
        });
    };
    var query = queryString_1.decodeScalar(location.query.query, '');
    var eventsFilterOptions = utils_2.getEventsFilterOptions(spanOperationBreakdownFilter, percentileValues);
    return (<SearchWrapper>
      <filter_1.default organization={organization} currentFilter={spanOperationBreakdownFilter} onChangeFilter={onChangeSpanOperationBreakdownFilter}/>
      <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
      <SearchRowMenuItem>
        <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Percentile') }} label={eventsFilterOptions[eventsDisplayFilterName].label}>
          {Object.entries(eventsFilterOptions).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), name = _b[0], filter = _b[1];
            return (<dropdownControl_1.DropdownItem key={name} onSelect={onChangeEventsDisplayFilter} eventKey={name} data-test-id={name} isActive={eventsDisplayFilterName === name}>
                {filter.label}
              </dropdownControl_1.DropdownItem>);
        })}
        </dropdownControl_1.default>
      </SearchRowMenuItem>
      <SearchRowMenuItem>
        <button_1.default to={eventView.getResultsViewUrlTarget(organization.slug)}>
          {locale_1.t('Open in Discover')}
        </button_1.default>
      </SearchRowMenuItem>
    </SearchWrapper>);
};
var SearchWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space_1.default(3));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/3;\n  margin: 0;\n"], ["\n  grid-column: 1/3;\n  margin: 0;\n"])));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledTable = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledSdkUpdatesAlert = styled_1.default(globalSdkUpdateAlert_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var SearchRowMenuItem = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  flex-grow: 0;\n"], ["\n  margin-left: ", ";\n  flex-grow: 0;\n"])), space_1.default(1));
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
exports.default = EventsPageContent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=content.jsx.map