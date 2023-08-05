Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var histogram_1 = tslib_1.__importDefault(require("app/utils/performance/histogram"));
var constants_1 = require("app/utils/performance/histogram/constants");
var queryString_1 = require("app/utils/queryString");
var header_1 = tslib_1.__importStar(require("../header"));
var constants_2 = require("./constants");
var vitalsPanel_1 = tslib_1.__importDefault(require("./vitalsPanel"));
var VitalsContent = /** @class */ (function (_super) {
    tslib_1.__extends(VitalsContent, _super);
    function VitalsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            delete queryParams.cursor;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: queryParams,
            });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        return _this;
    }
    VitalsContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, transactionName = _a.transactionName, location = _a.location, eventView = _a.eventView, projects = _a.projects, organization = _a.organization;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = queryString_1.decodeScalar(location.query.query, '');
        return (<React.Fragment>
        <header_1.default eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={header_1.Tab.RealUserMonitoring} hasWebVitals handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <histogram_1.default location={location} zoomKeys={constants_2.ZOOM_KEYS}>
          {function (_a) {
                var activeFilter = _a.activeFilter, handleFilterChange = _a.handleFilterChange, handleResetView = _a.handleResetView, isZoomed = _a.isZoomed;
                return (<Layout.Body>
                {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
                <Layout.Main fullWidth>
                  <StyledActions>
                    <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={_this.handleSearch}/>
                    <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Outliers') }} label={activeFilter.label}>
                      {constants_1.FILTER_OPTIONS.map(function (_a) {
                        var label = _a.label, value = _a.value;
                        return (<dropdownControl_1.DropdownItem key={value} onSelect={function (filterOption) {
                                analytics_1.trackAnalyticsEvent({
                                    eventKey: 'performance_views.vitals.filter_changed',
                                    eventName: 'Performance Views: Change vitals filter',
                                    organization_id: organization.id,
                                    value: filterOption,
                                });
                                handleFilterChange(filterOption);
                            }} eventKey={value} isActive={value === activeFilter.value}>
                          {label}
                        </dropdownControl_1.DropdownItem>);
                    })}
                    </dropdownControl_1.default>
                    <button_1.default onClick={function () {
                        analytics_1.trackAnalyticsEvent({
                            eventKey: 'performance_views.vitals.reset_view',
                            eventName: 'Performance Views: Reset vitals view',
                            organization_id: organization.id,
                        });
                        handleResetView();
                    }} disabled={!isZoomed} data-test-id="reset-view">
                      {locale_1.t('Reset View')}
                    </button_1.default>
                  </StyledActions>
                  <vitalsPanel_1.default organization={organization} location={location} eventView={eventView} dataFilter={activeFilter.value}/>
                </Layout.Main>
              </Layout.Body>);
            }}
        </histogram_1.default>
      </React.Fragment>);
    };
    return VitalsContent;
}(React.Component));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content max-content;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content max-content;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(2), space_1.default(3));
exports.default = VitalsContent;
var templateObject_1, templateObject_2;
//# sourceMappingURL=content.jsx.map