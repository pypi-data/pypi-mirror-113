Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var flatten_1 = tslib_1.__importDefault(require("lodash/flatten"));
var prompts_1 = require("app/actionCreators/prompts");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var createAlertButton_1 = tslib_1.__importDefault(require("app/components/createAlertButton"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
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
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var teamFilter_1 = tslib_1.__importStar(require("../rules/teamFilter"));
var header_1 = tslib_1.__importDefault(require("./header"));
var onboarding_1 = tslib_1.__importDefault(require("./onboarding"));
var row_1 = tslib_1.__importDefault(require("./row"));
var DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/?_ga=2.21848383.580096147.1592364314-1444595810.1582160976';
var IncidentsList = /** @class */ (function (_super) {
    tslib_1.__extends(IncidentsList, _super);
    function IncidentsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeSearch = function (title) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = tslib_1.__rest(_b, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { title: title }),
            });
        };
        _this.handleChangeFilter = function (sectionId, activeFilters) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = tslib_1.__rest(_b, ["cursor", "page"]);
            var team = currentQuery.team;
            if (sectionId === 'teams') {
                team = activeFilters.size ? tslib_1.__spreadArray([], tslib_1.__read(activeFilters)) : '';
            }
            var status = currentQuery.status;
            if (sectionId === 'status') {
                status = activeFilters.size ? tslib_1.__spreadArray([], tslib_1.__read(activeFilters)) : '';
            }
            router.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { status: status, 
                    // Preserve empty team query parameter
                    team: team.length === 0 ? '' : team }),
            });
        };
        return _this;
    }
    IncidentsList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
        var query = location.query;
        var status = this.getQueryStatus(query.status);
        // Filtering by one status, both does nothing
        if (status.length === 1) {
            query.status = status;
        }
        query.team = teamFilter_1.getTeamParams(query.team);
        if (organization.features.includes('alert-details-redesign')) {
            query.expand = ['original_alert_rule'];
        }
        return [['incidentList', "/organizations/" + (params === null || params === void 0 ? void 0 : params.orgId) + "/incidents/", { query: query }]];
    };
    IncidentsList.prototype.getQueryStatus = function (status) {
        if (Array.isArray(status)) {
            return status;
        }
        if (status === '') {
            return [];
        }
        return ['open', 'closed'].includes(status) ? [status] : [];
    };
    /**
     * If our incidentList is empty, determine if we've configured alert rules or
     * if the user has seen the welcome prompt.
     */
    IncidentsList.prototype.onLoadAllEndpointsSuccess = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var incidentList, _a, params, location, organization, alertRules, hasAlertRule, prompt, firstVisitShown;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        incidentList = this.state.incidentList;
                        if (!incidentList || incidentList.length !== 0) {
                            this.setState({ hasAlertRule: true, firstVisitShown: false });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + (params === null || params === void 0 ? void 0 : params.orgId) + "/alert-rules/", {
                                method: 'GET',
                                query: location.query,
                            })];
                    case 1:
                        alertRules = _b.sent();
                        hasAlertRule = alertRules.length > 0;
                        // We've already configured alert rules, no need to check if we should show
                        // the "first time welcome" prompt
                        if (hasAlertRule) {
                            this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: false, loading: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, prompts_1.promptsCheck(this.api, {
                                organizationId: organization.id,
                                feature: 'alert_stream',
                            })];
                    case 2:
                        prompt = _b.sent();
                        firstVisitShown = !(prompt === null || prompt === void 0 ? void 0 : prompt.dismissedTime);
                        if (firstVisitShown) {
                            // Prompt has not been seen, mark the prompt as seen immediately so they
                            // don't see it again
                            prompts_1.promptsUpdate(this.api, {
                                feature: 'alert_stream',
                                organizationId: organization.id,
                                status: 'dismissed',
                            });
                        }
                        this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: firstVisitShown, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    IncidentsList.prototype.renderFilterBar = function () {
        var _a;
        var _b = this.props, teams = _b.teams, location = _b.location;
        var selectedTeams = new Set(teamFilter_1.getTeamParams(location.query.team));
        var selectedStatus = new Set(this.getQueryStatus(location.query.status));
        return (<FilterWrapper>
        <teamFilter_1.default showStatus teams={teams} selectedStatus={selectedStatus} selectedTeams={selectedTeams} handleChangeFilter={this.handleChangeFilter}/>
        <StyledSearchBar placeholder={locale_1.t('Search by name')} query={(_a = location.query) === null || _a === void 0 ? void 0 : _a.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    };
    IncidentsList.prototype.tryRenderOnboarding = function () {
        var firstVisitShown = this.state.firstVisitShown;
        var organization = this.props.organization;
        if (!firstVisitShown) {
            return null;
        }
        var actions = (<react_1.Fragment>
        <button_1.default size="small" external href={DOCS_URL}>
          {locale_1.t('View Features')}
        </button_1.default>
        <createAlertButton_1.default organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="alert_stream">
          {locale_1.t('Create Alert Rule')}
        </createAlertButton_1.default>
      </react_1.Fragment>);
        return <onboarding_1.default actions={actions}/>;
    };
    IncidentsList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IncidentsList.prototype.renderList = function () {
        var _a;
        var _b = this.state, loading = _b.loading, incidentList = _b.incidentList, incidentListPageLinks = _b.incidentListPageLinks, hasAlertRule = _b.hasAlertRule;
        var _c = this.props, orgId = _c.params.orgId, organization = _c.organization;
        var allProjectsFromIncidents = new Set(flatten_1.default(incidentList === null || incidentList === void 0 ? void 0 : incidentList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var checkingForAlertRules = incidentList && incidentList.length === 0 && hasAlertRule === undefined
            ? true
            : false;
        var showLoadingIndicator = loading || checkingForAlertRules;
        return (<react_1.Fragment>
        {(_a = this.tryRenderOnboarding()) !== null && _a !== void 0 ? _a : (<panels_1.PanelTable isLoading={showLoadingIndicator} isEmpty={(incidentList === null || incidentList === void 0 ? void 0 : incidentList.length) === 0} emptyMessage={locale_1.t('No incidents exist for the current query.')} emptyAction={<EmptyStateAction>
                {locale_1.tct('Learn more about [link:Metric Alerts]', {
                        link: <externalLink_1.default href={DOCS_URL}/>,
                    })}
              </EmptyStateAction>} headers={[
                    locale_1.t('Alert Rule'),
                    locale_1.t('Triggered'),
                    locale_1.t('Duration'),
                    locale_1.t('Project'),
                    locale_1.t('Alert ID'),
                    locale_1.t('Team'),
                ]}>
            <projects_1.default orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {function (_a) {
                    var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                    return incidentList.map(function (incident) { return (<row_1.default key={incident.id} projectsLoaded={initiallyLoaded} projects={projects} incident={incident} orgId={orgId} organization={organization}/>); });
                }}
            </projects_1.default>
          </panels_1.PanelTable>)}
        <pagination_1.default pageLinks={incidentListPageLinks}/>
      </react_1.Fragment>);
    };
    IncidentsList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, router = _a.router;
        var orgId = params.orgId;
        return (<sentryDocumentTitle_1.default title={locale_1.t('Alerts')} orgSlug={orgId}>
        <globalSelectionHeader_1.default organization={organization} showDateSelector={false}>
          <header_1.default organization={organization} router={router} activeTab="stream"/>
          <StyledLayoutBody>
            <Layout.Main fullWidth>
              {!this.tryRenderOnboarding() && (<react_1.Fragment>
                  <feature_1.default features={['alert-details-redesign']} organization={organization}>
                    <StyledAlert icon={<icons_1.IconInfo />}>
                      {locale_1.t('This page only shows metric alerts.')}
                    </StyledAlert>
                  </feature_1.default>
                  {this.renderFilterBar()}
                </react_1.Fragment>)}
              {this.renderList()}
            </Layout.Main>
          </StyledLayoutBody>
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return IncidentsList;
}(asyncComponent_1.default));
var IncidentsListContainer = /** @class */ (function (_super) {
    tslib_1.__extends(IncidentsListContainer, _super);
    function IncidentsListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IncidentsListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    IncidentsListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.status) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.status)) {
            this.trackView();
        }
    };
    IncidentsListContainer.prototype.trackView = function () {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'alert_stream.viewed',
            eventName: 'Alert Stream: Viewed',
            organization_id: organization.id,
        });
    };
    IncidentsListContainer.prototype.renderNoAccess = function () {
        return (<Layout.Body>
        <Layout.Main fullWidth>
          <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
        </Layout.Main>
      </Layout.Body>);
    };
    IncidentsListContainer.prototype.render = function () {
        var organization = this.props.organization;
        return (<feature_1.default features={['organizations:incidents']} organization={organization} hookName="feature-disabled:alerts-page" renderDisabled={this.renderNoAccess}>
        <IncidentsList {...this.props}/>
      </feature_1.default>);
    };
    return IncidentsListContainer;
}(react_1.Component));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var FilterWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  margin-left: ", ";\n"], ["\n  flex-grow: 1;\n  margin-left: ", ";\n"])), space_1.default(1.5));
var StyledLayoutBody = styled_1.default(Layout.Body)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -20px;\n"], ["\n  margin-bottom: -20px;\n"])));
var EmptyStateAction = styled_1.default('p')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
exports.default = withOrganization_1.default(withTeams_1.default(IncidentsListContainer));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map