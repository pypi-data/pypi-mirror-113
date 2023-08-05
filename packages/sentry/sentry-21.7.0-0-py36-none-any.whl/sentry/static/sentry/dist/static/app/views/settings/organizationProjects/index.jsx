Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var queryString_1 = require("app/utils/queryString");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var settingsProjectItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsProjectItem"));
var projectStatsGraph_1 = tslib_1.__importDefault(require("./projectStatsGraph"));
var ITEMS_PER_PAGE = 50;
var OrganizationProjects = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationProjects, _super);
    function OrganizationProjects() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationProjects.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        var location = this.props.location;
        var query = queryString_1.decodeScalar(location.query.query);
        return [
            [
                'projectList',
                "/organizations/" + orgId + "/projects/",
                {
                    query: {
                        query: query,
                        per_page: ITEMS_PER_PAGE,
                    },
                },
            ],
            [
                'projectStats',
                "/organizations/" + orgId + "/stats/",
                {
                    query: {
                        since: new Date().getTime() / 1000 - 3600 * 24,
                        stat: 'generated',
                        group: 'project',
                        per_page: ITEMS_PER_PAGE,
                    },
                },
            ],
        ];
    };
    OrganizationProjects.prototype.getTitle = function () {
        var organization = this.props.organization;
        return routeTitle_1.default(locale_1.t('Projects'), organization.slug, false);
    };
    OrganizationProjects.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationProjects.prototype.renderBody = function () {
        var _a = this.state, projectList = _a.projectList, projectListPageLinks = _a.projectListPageLinks, projectStats = _a.projectStats;
        var organization = this.props.organization;
        var canCreateProjects = new Set(organization.access).has('project:admin');
        var action = (<button_1.default priority="primary" size="small" disabled={!canCreateProjects} title={!canCreateProjects
                ? locale_1.t('You do not have permission to create projects')
                : undefined} to={"/organizations/" + organization.slug + "/projects/new/"} icon={<icons_1.IconAdd size="xs" isCircled/>}>
        {locale_1.t('Create Project')}
      </button_1.default>);
        return (<React.Fragment>
        <settingsPageHeader_1.default title="Projects" action={action}/>
        <SearchWrapper>
          {this.renderSearchInput({
                updateRoute: true,
                placeholder: locale_1.t('Search Projects'),
                className: 'search',
            })}
        </SearchWrapper>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Projects')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {projectList ? (utils_1.sortProjects(projectList).map(function (project) { return (<GridPanelItem key={project.id}>
                  <ProjectListItemWrapper>
                    <settingsProjectItem_1.default project={project} organization={organization}/>
                  </ProjectListItemWrapper>
                  <ProjectStatsGraphWrapper>
                    {projectStats ? (<projectStatsGraph_1.default key={project.id} project={project} stats={projectStats[project.id]}/>) : (<placeholder_1.default height="25px"/>)}
                  </ProjectStatsGraphWrapper>
                </GridPanelItem>); })) : (<loadingIndicator_1.default />)}
            {projectList && projectList.length === 0 && (<emptyMessage_1.default>{locale_1.t('No projects found.')}</emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {projectListPageLinks && (<pagination_1.default pageLinks={projectListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    return OrganizationProjects;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationProjects);
var SearchWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var GridPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: 0;\n"])));
var ProjectListItemWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  flex: 1;\n"], ["\n  padding: ", ";\n  flex: 1;\n"])), space_1.default(2));
var ProjectStatsGraphWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  width: 25%;\n  margin-left: ", ";\n"], ["\n  padding: ", ";\n  width: 25%;\n  margin-left: ", ";\n"])), space_1.default(2), space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map