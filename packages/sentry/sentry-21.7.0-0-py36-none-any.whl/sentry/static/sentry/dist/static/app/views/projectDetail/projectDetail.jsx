Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var globalSelection_1 = require("app/actionCreators/globalSelection");
var tags_1 = require("app/actionCreators/tags");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var createAlertButton_1 = tslib_1.__importDefault(require("app/components/createAlertButton"));
var globalAppStoreConnectUpdateAlert_1 = tslib_1.__importDefault(require("app/components/globalAppStoreConnectUpdateAlert"));
var globalSdkUpdateAlert_1 = tslib_1.__importDefault(require("app/components/globalSdkUpdateAlert"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var missingProjectMembership_1 = tslib_1.__importDefault(require("app/components/projects/missingProjectMembership"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var projectScoreCards_1 = tslib_1.__importDefault(require("./projectScoreCards/projectScoreCards"));
var projectCharts_1 = tslib_1.__importDefault(require("./projectCharts"));
var projectFilters_1 = tslib_1.__importDefault(require("./projectFilters"));
var projectIssues_1 = tslib_1.__importDefault(require("./projectIssues"));
var projectLatestAlerts_1 = tslib_1.__importDefault(require("./projectLatestAlerts"));
var projectLatestReleases_1 = tslib_1.__importDefault(require("./projectLatestReleases"));
var projectQuickLinks_1 = tslib_1.__importDefault(require("./projectQuickLinks"));
var projectTeamAccess_1 = tslib_1.__importDefault(require("./projectTeamAccess"));
var ProjectDetail = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectDetail, _super);
    function ProjectDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleProjectChange = function (selectedProjects) {
            var _a = _this.props, projects = _a.projects, router = _a.router, location = _a.location, organization = _a.organization;
            var newlySelectedProject = projects.find(function (p) { return p.id === String(selectedProjects[0]); });
            // if we change project in global header, we need to sync the project slug in the URL
            if (newlySelectedProject === null || newlySelectedProject === void 0 ? void 0 : newlySelectedProject.id) {
                router.replace({
                    pathname: "/organizations/" + organization.slug + "/projects/" + newlySelectedProject.slug + "/",
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { project: newlySelectedProject.id, environment: undefined }),
                });
            }
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, router = _a.router, location = _a.location;
            router.replace({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: query }),
            });
        };
        _this.tagValueLoader = function (key, search) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var projectId = location.query.project;
            return tags_1.fetchTagValues(_this.api, organization.slug, key, search, projectId ? [projectId] : null, location.query);
        };
        return _this;
    }
    ProjectDetail.prototype.getTitle = function () {
        var params = this.props.params;
        return routeTitle_1.default(locale_1.t('Project %s', params.projectId), params.orgId, false);
    };
    ProjectDetail.prototype.componentDidMount = function () {
        this.syncProjectWithSlug();
        if (this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    };
    ProjectDetail.prototype.componentDidUpdate = function (prevProps) {
        this.syncProjectWithSlug();
        if (prevProps.location.query.project !== this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    };
    Object.defineProperty(ProjectDetail.prototype, "project", {
        get: function () {
            var _a = this.props, projects = _a.projects, params = _a.params;
            return projects.find(function (p) { return p.slug === params.projectId; });
        },
        enumerable: false,
        configurable: true
    });
    ProjectDetail.prototype.fetchSessionsExistence = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, organization, location, _b, projectId, query, response, _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, location = _a.location;
                        _b = location.query, projectId = _b.project, query = _b.query;
                        if (!projectId) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            hasSessions: null,
                        });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/sessions/", {
                                query: {
                                    project: projectId,
                                    field: 'sum(session)',
                                    statsPeriod: '90d',
                                    interval: '1d',
                                    query: query,
                                },
                            })];
                    case 2:
                        response = _d.sent();
                        this.setState({
                            hasSessions: response.groups[0].totals['sum(session)'] > 0,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ProjectDetail.prototype.syncProjectWithSlug = function () {
        var _a;
        var _b = this.props, router = _b.router, location = _b.location;
        var projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        if (projectId && projectId !== location.query.project) {
            // if someone visits /organizations/sentry/projects/javascript/ (without ?project=XXX) we need to update URL and globalSelection with the right project ID
            globalSelection_1.updateProjects([Number(projectId)], router);
        }
    };
    ProjectDetail.prototype.isProjectStabilized = function () {
        var _a;
        var _b = this.props, selection = _b.selection, location = _b.location;
        var projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        return (utils_1.defined(projectId) &&
            projectId === location.query.project &&
            projectId === String(selection.projects[0]));
    };
    ProjectDetail.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectDetail.prototype.renderNoAccess = function (project) {
        var organization = this.props.organization;
        return (<organization_1.PageContent>
        <missingProjectMembership_1.default organization={organization} projectSlug={project.slug}/>
      </organization_1.PageContent>);
    };
    ProjectDetail.prototype.renderProjectNotFound = function () {
        return (<organization_1.PageContent>
        <alert_1.default type="error" icon={<icons_1.IconWarning />}>
          {locale_1.t('This project could not be found.')}
        </alert_1.default>
      </organization_1.PageContent>);
    };
    ProjectDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, router = _a.router, loadingProjects = _a.loadingProjects, selection = _a.selection;
        var project = this.project;
        var hasSessions = this.state.hasSessions;
        var query = location.query.query;
        var hasPerformance = organization.features.includes('performance-view');
        var hasTransactions = hasPerformance && (project === null || project === void 0 ? void 0 : project.firstTransactionEvent);
        var isProjectStabilized = this.isProjectStabilized();
        var visibleCharts = ['chart1'];
        if (hasTransactions || hasSessions) {
            visibleCharts.push('chart2');
        }
        if (!loadingProjects && !project) {
            return this.renderProjectNotFound();
        }
        if (!loadingProjects && project && !project.hasAccess) {
            return this.renderNoAccess(project);
        }
        return (<globalSelectionHeader_1.default disableMultipleProjectSelection skipLoadLastUsed onUpdateProjects={this.handleProjectChange}>
        <lightWeightNoProjectMessage_1.default organization={organization}>
          <StyledPageContent>
            <Layout.Header>
              <Layout.HeaderContent>
                <breadcrumbs_1.default crumbs={[
                {
                    to: "/organizations/" + params.orgId + "/projects/",
                    label: locale_1.t('Projects'),
                },
                { label: locale_1.t('Project Details') },
            ]}/>
                <Layout.Title>
                  <textOverflow_1.default>
                    {project && (<idBadge_1.default project={project} avatarSize={28} displayName={params.projectId} disableLink/>)}
                  </textOverflow_1.default>
                </Layout.Title>
              </Layout.HeaderContent>

              <Layout.HeaderActions>
                <buttonBar_1.default gap={1}>
                  <button_1.default to={
            // if we are still fetching project, we can use project slug to build issue stream url and let the redirect handle it
            (project === null || project === void 0 ? void 0 : project.id)
                ? "/organizations/" + params.orgId + "/issues/?project=" + project.id
                : "/" + params.orgId + "/" + params.projectId}>
                    {locale_1.t('View All Issues')}
                  </button_1.default>
                  <createAlertButton_1.default organization={organization} projectSlug={params.projectId}/>
                  <button_1.default icon={<icons_1.IconSettings />} label={locale_1.t('Settings')} to={"/settings/" + params.orgId + "/projects/" + params.projectId + "/"}/>
                </buttonBar_1.default>
              </Layout.HeaderActions>
            </Layout.Header>

            <Layout.Body>
              <StyledSdkUpdatesAlert />
              <StyledGlobalAppStoreConnectUpdateAlert project={project} organization={organization}/>
              <Layout.Main>
                <feature_1.default features={['semver']} organization={organization}>
                  <ProjectFiltersWrapper>
                    <projectFilters_1.default query={query} onSearch={this.handleSearch} tagValueLoader={this.tagValueLoader}/>
                  </ProjectFiltersWrapper>
                </feature_1.default>

                <projectScoreCards_1.default organization={organization} isProjectStabilized={isProjectStabilized} selection={selection} hasSessions={hasSessions} hasTransactions={hasTransactions} query={query}/>
                {isProjectStabilized && (<react_1.Fragment>
                    {visibleCharts.map(function (id, index) { return (<projectCharts_1.default location={location} organization={organization} router={router} key={"project-charts-" + id} chartId={id} chartIndex={index} projectId={project === null || project === void 0 ? void 0 : project.id} hasSessions={hasSessions} hasTransactions={!!hasTransactions} visibleCharts={visibleCharts} query={query}/>); })}
                    <projectIssues_1.default organization={organization} location={location} projectId={selection.projects[0]} query={query} api={this.api}/>
                  </react_1.Fragment>)}
              </Layout.Main>
              <Layout.Side>
                <projectTeamAccess_1.default organization={organization} project={project}/>
                <feature_1.default features={['incidents']} organization={organization}>
                  <projectLatestAlerts_1.default organization={organization} projectSlug={params.projectId} location={location} isProjectStabilized={isProjectStabilized}/>
                </feature_1.default>
                <projectLatestReleases_1.default organization={organization} projectSlug={params.projectId} projectId={project === null || project === void 0 ? void 0 : project.id} location={location} isProjectStabilized={isProjectStabilized}/>
                <projectQuickLinks_1.default organization={organization} project={project} location={location}/>
              </Layout.Side>
            </Layout.Body>
          </StyledPageContent>
        </lightWeightNoProjectMessage_1.default>
      </globalSelectionHeader_1.default>);
    };
    return ProjectDetail;
}(asyncView_1.default));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var ProjectFiltersWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var StyledSdkUpdatesAlert = styled_1.default(globalSdkUpdateAlert_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
var StyledGlobalAppStoreConnectUpdateAlert = styled_1.default(globalAppStoreConnectUpdateAlert_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledGlobalAppStoreConnectUpdateAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
exports.default = withProjects_1.default(withGlobalSelection_1.default(ProjectDetail));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=projectDetail.jsx.map