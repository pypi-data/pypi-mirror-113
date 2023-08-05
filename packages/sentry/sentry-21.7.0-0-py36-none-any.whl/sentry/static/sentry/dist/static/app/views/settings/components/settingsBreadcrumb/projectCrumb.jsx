Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectCrumb = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var breadcrumbDropdown_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
var findFirstRouteWithoutRouteParam_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/findFirstRouteWithoutRouteParam"));
var menuItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
var _1 = require(".");
var ProjectCrumb = function (_a) {
    var latestOrganization = _a.organization, latestProject = _a.project, projects = _a.projects, params = _a.params, routes = _a.routes, route = _a.route, props = tslib_1.__rest(_a, ["organization", "project", "projects", "params", "routes", "route"]);
    var handleSelect = function (item) {
        // We have to make exceptions for routes like "Project Alerts Rule Edit" or "Client Key Details"
        // Since these models are project specific, we need to traverse up a route when switching projects
        //
        // we manipulate `routes` so that it doesn't include the current project's route
        // which, unlike the org version, does not start with a route param
        var returnTo = findFirstRouteWithoutRouteParam_1.default(routes.slice(routes.indexOf(route) + 1), route);
        if (returnTo === undefined) {
            return;
        }
        react_router_1.browserHistory.push(recreateRoute_1.default(returnTo, { routes: routes, params: tslib_1.__assign(tslib_1.__assign({}, params), { projectId: item.value }) }));
    };
    if (!latestOrganization) {
        return null;
    }
    if (!projects) {
        return null;
    }
    var hasMenu = projects && projects.length > 1;
    return (<breadcrumbDropdown_1.default hasMenu={hasMenu} route={route} name={<ProjectName>
          {!latestProject ? (<loadingIndicator_1.default mini/>) : (<_1.CrumbLink to={replaceRouterParams_1.default('/settings/:orgId/projects/:projectId/', {
                    orgId: latestOrganization.slug,
                    projectId: latestProject.slug,
                })}>
              <idBadge_1.default project={latestProject} avatarSize={18} disableLink/>
            </_1.CrumbLink>)}
        </ProjectName>} onSelect={handleSelect} items={projects.map(function (project, index) { return ({
            index: index,
            value: project.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default project={project} avatarProps={{ consistentWidth: true }} avatarSize={18} disableLink/>
          </menuItem_1.default>),
        }); })} {...props}/>);
};
exports.ProjectCrumb = ProjectCrumb;
exports.default = withProjects_1.default(withLatestContext_1.default(ProjectCrumb));
// Set height of crumb because of spinner
var SPINNER_SIZE = '24px';
var ProjectName = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n\n  .loading {\n    width: ", ";\n    height: ", ";\n    margin: 0 ", " 0 0;\n  }\n"], ["\n  display: flex;\n\n  .loading {\n    width: ", ";\n    height: ", ";\n    margin: 0 ", " 0 0;\n  }\n"])), SPINNER_SIZE, SPINNER_SIZE, space_1.default(0.25));
var templateObject_1;
//# sourceMappingURL=projectCrumb.jsx.map