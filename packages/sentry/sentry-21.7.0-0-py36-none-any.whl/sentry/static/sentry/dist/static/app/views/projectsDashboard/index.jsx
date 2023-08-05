Object.defineProperty(exports, "__esModule", { value: true });
exports.Dashboard = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_lazyload_1 = tslib_1.__importDefault(require("react-lazyload"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var react_2 = require("@sentry/react");
var flatten_1 = tslib_1.__importDefault(require("lodash/flatten"));
var uniqBy_1 = tslib_1.__importDefault(require("lodash/uniqBy"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var noProjectMessage_1 = tslib_1.__importDefault(require("app/components/noProjectMessage"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var projectsStatsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStatsStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeamsForUser_1 = tslib_1.__importDefault(require("app/utils/withTeamsForUser"));
var resources_1 = tslib_1.__importDefault(require("./resources"));
var teamSection_1 = tslib_1.__importDefault(require("./teamSection"));
var Dashboard = /** @class */ (function (_super) {
    tslib_1.__extends(Dashboard, _super);
    function Dashboard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Dashboard.prototype.componentWillUnmount = function () {
        projectsStatsStore_1.default.reset();
    };
    Dashboard.prototype.render = function () {
        var _a = this.props, teams = _a.teams, params = _a.params, organization = _a.organization, loadingTeams = _a.loadingTeams, error = _a.error;
        if (loadingTeams) {
            return <loadingIndicator_1.default />;
        }
        if (error) {
            return <loadingError_1.default message="An error occurred while fetching your projects"/>;
        }
        var filteredTeams = teams.filter(function (team) { return team.projects.length; });
        filteredTeams.sort(function (team1, team2) { return team1.slug.localeCompare(team2.slug); });
        var projects = uniqBy_1.default(flatten_1.default(teams.map(function (teamObj) { return teamObj.projects; })), 'id');
        var favorites = projects.filter(function (project) { return project.isBookmarked; });
        var access = new Set(organization.access);
        var canCreateProjects = access.has('project:admin');
        var hasTeamAdminAccess = access.has('team:admin');
        var showEmptyMessage = projects.length === 0 && favorites.length === 0;
        var showResources = projects.length === 1 && !projects[0].firstEvent;
        if (showEmptyMessage) {
            return (<noProjectMessage_1.default organization={organization} projects={projects} superuserNeedsToBeProjectMember>
          {null}
        </noProjectMessage_1.default>);
        }
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={locale_1.t('Projects Dashboard')} orgSlug={organization.slug}/>
        {projects.length > 0 && (<ProjectsHeader>
            <pageHeading_1.default>Projects</pageHeading_1.default>
            <button_1.default size="small" disabled={!canCreateProjects} title={!canCreateProjects
                    ? locale_1.t('You do not have permission to create projects')
                    : undefined} to={"/organizations/" + organization.slug + "/projects/new/"} icon={<icons_1.IconAdd size="xs" isCircled/>} data-test-id="create-project">
              {locale_1.t('Create Project')}
            </button_1.default>
          </ProjectsHeader>)}

        {filteredTeams.map(function (team, index) {
                var showBorder = index !== teams.length - 1;
                return (<react_lazyload_1.default key={team.slug} once debounce={50} height={300} offset={300}>
              <teamSection_1.default orgId={params.orgId} team={team} showBorder={showBorder} title={hasTeamAdminAccess ? (<TeamLink to={"/settings/" + organization.slug + "/teams/" + team.slug + "/"}>
                      <idBadge_1.default team={team} avatarSize={22}/>
                    </TeamLink>) : (<idBadge_1.default team={team} avatarSize={22}/>)} projects={utils_1.sortProjects(team.projects)} access={access}/>
            </react_lazyload_1.default>);
            })}

        {showResources && <resources_1.default organization={organization}/>}
      </react_1.Fragment>);
    };
    return Dashboard;
}(react_1.Component));
exports.Dashboard = Dashboard;
var OrganizationDashboard = function (props) { return (<OrganizationDashboardWrapper>
    <Dashboard {...props}/>
  </OrganizationDashboardWrapper>); };
var TeamLink = styled_1.default(react_router_1.Link)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var ProjectsHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  padding: ", " ", " 0 ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])), space_1.default(3), space_1.default(4), space_1.default(4));
var OrganizationDashboardWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
exports.default = withApi_1.default(withOrganization_1.default(withTeamsForUser_1.default(react_2.withProfiler(OrganizationDashboard))));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map