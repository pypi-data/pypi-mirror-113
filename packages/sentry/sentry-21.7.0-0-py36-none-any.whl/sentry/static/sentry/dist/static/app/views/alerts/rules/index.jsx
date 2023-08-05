Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var flatten_1 = tslib_1.__importDefault(require("lodash/flatten"));
var indicator_1 = require("app/actionCreators/indicator");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var header_1 = tslib_1.__importDefault(require("../list/header"));
var utils_1 = require("../utils");
var row_1 = tslib_1.__importDefault(require("./row"));
var teamFilter_1 = tslib_1.__importStar(require("./teamFilter"));
var DOCS_URL = 'https://docs.sentry.io/product/alerts-notifications/metric-alerts/';
var AlertRulesList = /** @class */ (function (_super) {
    tslib_1.__extends(AlertRulesList, _super);
    function AlertRulesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeFilter = function (_sectionId, activeFilters) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = tslib_1.__rest(_b, ["cursor", "page"]);
            var teams = tslib_1.__spreadArray([], tslib_1.__read(activeFilters));
            router.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { team: teams.length ? teams : '' }),
            });
        };
        _this.handleChangeSearch = function (name) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = tslib_1.__rest(_b, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { name: name }),
            });
        };
        _this.handleDeleteRule = function (projectId, rule) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var params, orgId, alertPath, _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId;
                        alertPath = utils_1.isIssueAlert(rule) ? 'rules' : 'alert-rules';
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/" + alertPath + "/" + rule.id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        this.reloadData();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('Error deleting rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRulesList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
        var query = location.query;
        if (organization.features.includes('alert-details-redesign')) {
            query.expand = ['latestIncident'];
        }
        query.team = teamFilter_1.getTeamParams(query.team);
        if (organization.features.includes('alert-details-redesign') && !query.sort) {
            query.sort = ['incident_status', 'date_triggered'];
        }
        return [
            [
                'ruleList',
                "/organizations/" + (params && params.orgId) + "/combined-rules/",
                {
                    query: query,
                },
            ],
        ];
    };
    AlertRulesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    AlertRulesList.prototype.renderFilterBar = function () {
        var _a;
        var _b = this.props, teams = _b.teams, location = _b.location;
        var selectedTeams = new Set(teamFilter_1.getTeamParams(location.query.team));
        return (<FilterWrapper>
        <teamFilter_1.default teams={teams} selectedTeams={selectedTeams} handleChangeFilter={this.handleChangeFilter}/>
        <StyledSearchBar placeholder={locale_1.t('Search by name')} query={(_a = location.query) === null || _a === void 0 ? void 0 : _a.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    };
    AlertRulesList.prototype.renderList = function () {
        var _this = this;
        var _a = this.props, orgId = _a.params.orgId, query = _a.location.query, organization = _a.organization, teams = _a.teams;
        var _b = this.state, loading = _b.loading, _c = _b.ruleList, ruleList = _c === void 0 ? [] : _c, ruleListPageLinks = _b.ruleListPageLinks;
        var allProjectsFromIncidents = new Set(flatten_1.default(ruleList === null || ruleList === void 0 ? void 0 : ruleList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var sort = {
            asc: query.asc === '1',
            field: query.sort || 'date_added',
        };
        var _cursor = query.cursor, _page = query.page, currentQuery = tslib_1.__rest(query, ["cursor", "page"]);
        var hasAlertList = organization.features.includes('alert-details-redesign');
        var isAlertRuleSort = sort.field.includes('incident_status') || sort.field.includes('date_triggered');
        var sortArrow = (<icons_1.IconArrow color="gray300" size="xs" direction={sort.asc ? 'up' : 'down'}/>);
        var userTeams = new Set(teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        }));
        return (<StyledLayoutBody>
        <Layout.Main fullWidth>
          {this.renderFilterBar()}
          <StyledPanelTable headers={tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((hasAlertList
                ? [
                    // eslint-disable-next-line react/jsx-key
                    <StyledSortLink to={{
                            pathname: location.pathname,
                            query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { asc: sort.field === 'name' && !sort.asc ? '1' : undefined, sort: 'name' }),
                        }}>
                      {locale_1.t('Alert Rule')} {sort.field === 'name' && sortArrow}
                    </StyledSortLink>,
                    // eslint-disable-next-line react/jsx-key
                    <StyledSortLink to={{
                            pathname: location.pathname,
                            query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { asc: isAlertRuleSort && !sort.asc ? '1' : undefined, sort: ['incident_status', 'date_triggered'] }),
                        }}>
                      {locale_1.t('Status')} {isAlertRuleSort && sortArrow}
                    </StyledSortLink>,
                ]
                : [
                    locale_1.t('Type'),
                    // eslint-disable-next-line react/jsx-key
                    <StyledSortLink to={{
                            pathname: location.pathname,
                            query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { asc: sort.field === 'name' && !sort.asc ? '1' : undefined, sort: 'name' }),
                        }}>
                      {locale_1.t('Alert Name')} {sort.field === 'name' && sortArrow}
                    </StyledSortLink>,
                ]))), [
                locale_1.t('Project'),
                locale_1.t('Team')
            ]), tslib_1.__read((hasAlertList ? [] : [locale_1.t('Created By')]))), [
                // eslint-disable-next-line react/jsx-key
                <StyledSortLink to={{
                        pathname: location.pathname,
                        query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { asc: sort.field === 'date_added' && !sort.asc ? '1' : undefined, sort: 'date_added' }),
                    }}>
                {locale_1.t('Created')} {sort.field === 'date_added' && sortArrow}
              </StyledSortLink>,
                locale_1.t('Actions'),
            ])} isLoading={loading} isEmpty={(ruleList === null || ruleList === void 0 ? void 0 : ruleList.length) === 0} emptyMessage={locale_1.t('No alert rules found for the current query.')} emptyAction={<EmptyStateAction>
                {locale_1.tct('Learn more about [link:Alerts]', {
                    link: <externalLink_1.default href={DOCS_URL}/>,
                })}
              </EmptyStateAction>} hasAlertList={hasAlertList}>
            <projects_1.default orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {function (_a) {
                var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                return ruleList.map(function (rule) { return (<row_1.default 
                // Metric and issue alerts can have the same id
                key={(utils_1.isIssueAlert(rule) ? 'metric' : 'issue') + "-" + rule.id} projectsLoaded={initiallyLoaded} projects={projects} rule={rule} orgId={orgId} onDelete={_this.handleDeleteRule} organization={organization} userTeams={userTeams}/>); });
            }}
            </projects_1.default>
          </StyledPanelTable>
          <pagination_1.default pageLinks={ruleListPageLinks}/>
        </Layout.Main>
      </StyledLayoutBody>);
    };
    AlertRulesList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, router = _a.router;
        var orgId = params.orgId;
        return (<sentryDocumentTitle_1.default title={locale_1.t('Alerts')} orgSlug={orgId}>
        <globalSelectionHeader_1.default organization={organization} showDateSelector={false} showEnvironmentSelector={false}>
          <header_1.default organization={organization} router={router} activeTab="rules"/>
          {this.renderList()}
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return AlertRulesList;
}(asyncComponent_1.default));
var AlertRulesListContainer = /** @class */ (function (_super) {
    tslib_1.__extends(AlertRulesListContainer, _super);
    function AlertRulesListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertRulesListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    AlertRulesListContainer.prototype.componentDidUpdate = function (prevProps) {
        var _a, _b;
        var location = this.props.location;
        if (((_a = prevProps.location.query) === null || _a === void 0 ? void 0 : _a.sort) !== ((_b = location.query) === null || _b === void 0 ? void 0 : _b.sort)) {
            this.trackView();
        }
    };
    AlertRulesListContainer.prototype.trackView = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'alert_rules.viewed',
            eventName: 'Alert Rules: Viewed',
            organization_id: organization.id,
            sort: Array.isArray(location.query.sort)
                ? location.query.sort.join(',')
                : location.query.sort,
        });
    };
    AlertRulesListContainer.prototype.render = function () {
        return <AlertRulesList {...this.props}/>;
    };
    return AlertRulesListContainer;
}(react_1.Component));
exports.default = withGlobalSelection_1.default(withTeams_1.default(AlertRulesListContainer));
var StyledLayoutBody = styled_1.default(Layout.Body)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -20px;\n"], ["\n  margin-bottom: -20px;\n"])));
var StyledSortLink = styled_1.default(link_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"], ["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"])));
var FilterWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  margin-left: ", ";\n"], ["\n  flex-grow: 1;\n  margin-left: ", ";\n"])), space_1.default(1.5));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  overflow: auto;\n  @media (min-width: ", ") {\n    overflow: initial;\n  }\n\n  grid-template-columns: auto 1.5fr 1fr 1fr ", " 1fr auto;\n  white-space: nowrap;\n  font-size: ", ";\n"], ["\n  overflow: auto;\n  @media (min-width: ", ") {\n    overflow: initial;\n  }\n\n  grid-template-columns: auto 1.5fr 1fr 1fr ", " 1fr auto;\n  white-space: nowrap;\n  font-size: ", ";\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return (!p.hasAlertList ? '1fr' : ''); }, function (p) { return p.theme.fontSizeMedium; });
var EmptyStateAction = styled_1.default('p')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map