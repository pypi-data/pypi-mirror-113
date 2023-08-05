Object.defineProperty(exports, "__esModule", { value: true });
exports.DiscoverLanding = exports.StyledPageHeader = void 0;
var tslib_1 = require("tslib");
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var query_string_1 = require("query-string");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var queryString_1 = require("app/utils/queryString");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var banner_1 = tslib_1.__importDefault(require("./banner"));
var data_1 = require("./data");
var queryList_1 = tslib_1.__importDefault(require("./queryList"));
var utils_1 = require("./utils");
var SORT_OPTIONS = [
    { label: locale_1.t('My Queries'), value: 'myqueries' },
    { label: locale_1.t('Recently Edited'), value: '-dateUpdated' },
    { label: locale_1.t('Query Name (A-Z)'), value: 'name' },
    { label: locale_1.t('Date Created (Newest)'), value: '-dateCreated' },
    { label: locale_1.t('Date Created (Oldest)'), value: 'dateCreated' },
    { label: locale_1.t('Most Outdated'), value: 'dateUpdated' },
];
var DiscoverLanding = /** @class */ (function (_super) {
    tslib_1.__extends(DiscoverLanding, _super);
    function DiscoverLanding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            // local component state
            renderPrebuilt: utils_1.shouldRenderPrebuilt(),
            savedQueries: null,
            savedQueriesPageLinks: '',
        };
        _this.shouldReload = true;
        _this.handleQueryChange = function () {
            _this.fetchData({ reloading: true });
        };
        _this.handleSearchQuery = function (searchQuery) {
            var location = _this.props.location;
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        _this.handleSortChange = function (value) {
            var location = _this.props.location;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.change_sort',
                eventName: 'Discoverv2: Sort By Changed',
                organization_id: parseInt(_this.props.organization.id, 10),
                sort: value,
            });
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
        _this.togglePrebuilt = function () {
            var renderPrebuilt = _this.state.renderPrebuilt;
            _this.setState({ renderPrebuilt: !renderPrebuilt }, function () {
                utils_1.setRenderPrebuilt(!renderPrebuilt);
                _this.fetchData({ reloading: true });
            });
        };
        _this.onGoLegacyDiscover = function () {
            localStorage.setItem('discover:version', '1');
            var user = configStore_1.default.get('user');
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.opt_out',
                eventName: 'Discoverv2: Go to discover',
                organization_id: parseInt(_this.props.organization.id, 10),
                user_id: parseInt(user.id, 10),
            });
        };
        return _this;
    }
    DiscoverLanding.prototype.getSavedQuerySearchQuery = function () {
        var location = this.props.location;
        return queryString_1.decodeScalar(location.query.query, '').trim();
    };
    DiscoverLanding.prototype.getActiveSort = function () {
        var location = this.props.location;
        var urlSort = queryString_1.decodeScalar(location.query.sort, 'myqueries');
        return SORT_OPTIONS.find(function (item) { return item.value === urlSort; }) || SORT_OPTIONS[0];
    };
    DiscoverLanding.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var views = utils_1.getPrebuiltQueries(organization);
        var searchQuery = this.getSavedQuerySearchQuery();
        var cursor = queryString_1.decodeScalar(location.query.cursor);
        var perPage = 9;
        var canRenderPrebuilt = this.state
            ? this.state.renderPrebuilt
            : utils_1.shouldRenderPrebuilt();
        if (!cursor && canRenderPrebuilt) {
            // invariant: we're on the first page
            if (searchQuery && searchQuery.length > 0) {
                var needleSearch_1 = searchQuery.toLowerCase();
                var numOfPrebuiltQueries = views.reduce(function (sum, view) {
                    var eventView = eventView_1.default.fromNewQueryWithLocation(view, location);
                    // if a search is performed on the list of queries, we filter
                    // on the pre-built queries
                    if (eventView.name && eventView.name.toLowerCase().includes(needleSearch_1)) {
                        return sum + 1;
                    }
                    return sum;
                }, 0);
                perPage = Math.max(1, perPage - numOfPrebuiltQueries);
            }
            else {
                perPage = Math.max(1, perPage - views.length);
            }
        }
        var queryParams = {
            cursor: cursor,
            query: "version:2 name:\"" + searchQuery + "\"",
            per_page: perPage.toString(),
            sortBy: this.getActiveSort().value,
        };
        if (!cursor) {
            delete queryParams.cursor;
        }
        return [
            [
                'savedQueries',
                "/organizations/" + organization.slug + "/discover/saved/",
                {
                    query: queryParams,
                },
            ],
        ];
    };
    DiscoverLanding.prototype.componentDidUpdate = function (prevProps) {
        var PAYLOAD_KEYS = ['sort', 'cursor', 'query'];
        var payloadKeysChanged = !isEqual_1.default(pick_1.default(prevProps.location.query, PAYLOAD_KEYS), pick_1.default(this.props.location.query, PAYLOAD_KEYS));
        // if any of the query strings relevant for the payload has changed,
        // we re-fetch data
        if (payloadKeysChanged) {
            this.fetchData();
        }
    };
    DiscoverLanding.prototype.renderBanner = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var eventView = eventView_1.default.fromNewQueryWithLocation(data_1.DEFAULT_EVENT_VIEW, location);
        var to = eventView.getResultsViewUrlTarget(organization.slug);
        var resultsUrl = to.pathname + "?" + query_string_1.stringify(to.query);
        return <banner_1.default organization={organization} resultsUrl={resultsUrl}/>;
    };
    DiscoverLanding.prototype.renderActions = function () {
        var _this = this;
        var activeSort = this.getActiveSort();
        var _a = this.state, renderPrebuilt = _a.renderPrebuilt, savedQueries = _a.savedQueries;
        return (<StyledActions>
        <StyledSearchBar defaultQuery="" query={this.getSavedQuerySearchQuery()} placeholder={locale_1.t('Search saved queries')} onSearch={this.handleSearchQuery}/>
        <PrebuiltSwitch>
          <SwitchLabel>Show Prebuilt</SwitchLabel>
          <switchButton_1.default isActive={renderPrebuilt} isDisabled={renderPrebuilt && (savedQueries !== null && savedQueries !== void 0 ? savedQueries : []).length === 0} size="lg" toggle={this.togglePrebuilt}/>
        </PrebuiltSwitch>
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
    DiscoverLanding.prototype.renderNoAccess = function () {
        return (<organization_1.PageContent>
        <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
      </organization_1.PageContent>);
    };
    DiscoverLanding.prototype.renderBody = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var _b = this.state, savedQueries = _b.savedQueries, savedQueriesPageLinks = _b.savedQueriesPageLinks, renderPrebuilt = _b.renderPrebuilt;
        return (<queryList_1.default pageLinks={savedQueriesPageLinks} savedQueries={savedQueries !== null && savedQueries !== void 0 ? savedQueries : []} savedQuerySearchQuery={this.getSavedQuerySearchQuery()} renderPrebuilt={renderPrebuilt} location={location} organization={organization} onQueryChange={this.handleQueryChange}/>);
    };
    DiscoverLanding.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization;
        var eventView = eventView_1.default.fromNewQueryWithLocation(data_1.DEFAULT_EVENT_VIEW, location);
        var to = eventView.getResultsViewUrlTarget(organization.slug);
        return (<feature_1.default organization={organization} features={['discover-query']} renderDisabled={this.renderNoAccess}>
        <sentryDocumentTitle_1.default title={locale_1.t('Discover')} orgSlug={organization.slug}>
          <StyledPageContent>
            <lightWeightNoProjectMessage_1.default organization={organization}>
              <organization_1.PageContent>
                <exports.StyledPageHeader>
                  <guideAnchor_1.default target="discover_landing_header">
                    {locale_1.t('Discover')}
                  </guideAnchor_1.default>
                  <StyledButton data-test-id="build-new-query" to={to} priority="primary" onClick={function () {
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'discover_v2.build_new_query',
                    eventName: 'Discoverv2: Build a new Discover Query',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
            }}>
                    {locale_1.t('Build a new query')}
                  </StyledButton>
                </exports.StyledPageHeader>
                {this.renderBanner()}
                {this.renderActions()}
                {this.renderComponent()}
              </organization_1.PageContent>
            </lightWeightNoProjectMessage_1.default>
          </StyledPageContent>
        </sentryDocumentTitle_1.default>
      </feature_1.default>);
    };
    return DiscoverLanding;
}(asyncComponent_1.default));
exports.DiscoverLanding = DiscoverLanding;
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var PrebuiltSwitch = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var SwitchLabel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding-right: 8px;\n"], ["\n  padding-right: 8px;\n"])));
exports.StyledPageHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space_1.default(2));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content min-content;\n  align-items: center;\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content min-content;\n  align-items: center;\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n"])), space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var StyledButton = styled_1.default(button_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
exports.default = withOrganization_1.default(DiscoverLanding);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=landing.jsx.map