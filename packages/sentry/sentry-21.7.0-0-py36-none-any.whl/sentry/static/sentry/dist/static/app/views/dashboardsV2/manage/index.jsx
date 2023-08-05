Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var dashboardList_1 = tslib_1.__importDefault(require("./dashboardList"));
var SORT_OPTIONS = [
    { label: locale_1.t('My Dashboards'), value: 'mydashboards' },
    { label: locale_1.t('Dashboard Name (A-Z)'), value: 'title' },
    { label: locale_1.t('Date Created (Newest)'), value: '-dateCreated' },
    { label: locale_1.t('Date Created (Oldest)'), value: 'dateCreated' },
];
var ManageDashboards = /** @class */ (function (_super) {
    tslib_1.__extends(ManageDashboards, _super);
    function ManageDashboards() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSortChange = function (value) {
            var location = _this.props.location;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'dashboards_manage.change_sort',
                eventName: 'Dashboards Manager: Sort By Changed',
                organization_id: parseInt(_this.props.organization.id, 10),
                sort: value,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
        return _this;
    }
    ManageDashboards.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        return [
            [
                'dashboards',
                "/organizations/" + organization.slug + "/dashboards/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, ['cursor', 'query'])), { sort: this.getActiveSort().value, per_page: '9' }),
                },
            ],
        ];
    };
    ManageDashboards.prototype.getActiveSort = function () {
        var location = this.props.location;
        var urlSort = queryString_1.decodeScalar(location.query.sort, 'mydashboards');
        return SORT_OPTIONS.find(function (item) { return item.value === urlSort; }) || SORT_OPTIONS[0];
    };
    ManageDashboards.prototype.onDashboardsChange = function () {
        this.reloadData();
    };
    ManageDashboards.prototype.handleSearch = function (query) {
        var _a = this.props, location = _a.location, router = _a.router;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'dashboards_manage.search',
            eventName: 'Dashboards Manager: Search',
            organization_id: parseInt(this.props.organization.id, 10),
        });
        router.push({
            pathname: location.pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: query }),
        });
    };
    ManageDashboards.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ManageDashboards.prototype.renderActions = function () {
        var _this = this;
        var activeSort = this.getActiveSort();
        return (<StyledActions>
        <searchBar_1.default defaultQuery="" query={this.getQuery()} placeholder={locale_1.t('Search Dashboards')} onSearch={function (query) { return _this.handleSearch(query); }}/>
        <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Sort By') }} label={activeSort.label}>
          {SORT_OPTIONS.map(function (_a) {
                var label = _a.label, value = _a.value;
                return (<dropdownControl_1.DropdownItem key={value} onSelect={_this.handleSortChange} eventKey={value} isActive={value === activeSort.value}>
              {label}
            </dropdownControl_1.DropdownItem>);
            })}
        </dropdownControl_1.default>
      </StyledActions>);
    };
    ManageDashboards.prototype.renderNoAccess = function () {
        return (<organization_1.PageContent>
        <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
      </organization_1.PageContent>);
    };
    ManageDashboards.prototype.renderDashboards = function () {
        var _this = this;
        var _a = this.state, dashboards = _a.dashboards, dashboardsPageLinks = _a.dashboardsPageLinks;
        var _b = this.props, organization = _b.organization, location = _b.location, api = _b.api;
        return (<dashboardList_1.default api={api} dashboards={dashboards} organization={organization} pageLinks={dashboardsPageLinks} location={location} onDashboardsChange={function () { return _this.onDashboardsChange(); }}/>);
    };
    ManageDashboards.prototype.getTitle = function () {
        return locale_1.t('Dashboards');
    };
    ManageDashboards.prototype.onCreate = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'dashboards_manage.create.start',
            eventName: 'Dashboards Manager: Dashboard Create Started',
            organization_id: parseInt(organization.id, 10),
        });
        react_router_1.browserHistory.push({
            pathname: "/organizations/" + organization.slug + "/dashboards/new/",
            query: location.query,
        });
    };
    ManageDashboards.prototype.renderBody = function () {
        var _this = this;
        var organization = this.props.organization;
        return (<feature_1.default organization={organization} features={['dashboards-edit']} renderDisabled={this.renderNoAccess}>
        <sentryDocumentTitle_1.default title={locale_1.t('Dashboards')} orgSlug={organization.slug}>
          <StyledPageContent>
            <lightWeightNoProjectMessage_1.default organization={organization}>
              <organization_1.PageContent>
                <StyledPageHeader>
                  {locale_1.t('Dashboards')}
                  <button_1.default data-test-id="dashboard-create" onClick={function (event) {
                event.preventDefault();
                _this.onCreate();
            }} priority="primary" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                    {locale_1.t('Create Dashboard')}
                  </button_1.default>
                </StyledPageHeader>
                {this.renderActions()}
                {this.renderDashboards()}
              </organization_1.PageContent>
            </lightWeightNoProjectMessage_1.default>
          </StyledPageContent>
        </sentryDocumentTitle_1.default>
      </feature_1.default>);
    };
    return ManageDashboards;
}(asyncView_1.default));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledPageHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space_1.default(2));
var StyledActions = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n"])), space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
exports.default = withApi_1.default(withOrganization_1.default(ManageDashboards));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map