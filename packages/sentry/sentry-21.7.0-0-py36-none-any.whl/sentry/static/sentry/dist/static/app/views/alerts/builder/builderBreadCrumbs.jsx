Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var menuItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
function BuilderBreadCrumbs(props) {
    var orgSlug = props.orgSlug, title = props.title, alertName = props.alertName, projectSlug = props.projectSlug, projects = props.projects, routes = props.routes, canChangeProject = props.canChangeProject, location = props.location;
    var project = projects.find(function (_a) {
        var slug = _a.slug;
        return projectSlug === slug;
    });
    var isSuperuser = isActiveSuperuser_1.isActiveSuperuser();
    var projectCrumbLink = {
        to: "/settings/" + orgSlug + "/projects/" + projectSlug + "/",
        label: <idBadge_1.default project={project} avatarSize={18} disableLink/>,
        preserveGlobalSelection: true,
    };
    var projectCrumbDropdown = {
        onSelect: function (_a) {
            var value = _a.value;
            react_router_1.browserHistory.push(recreateRoute_1.default('', {
                routes: routes,
                params: { orgId: orgSlug, projectId: value },
                location: location,
            }));
        },
        label: <idBadge_1.default project={project} avatarSize={18} disableLink/>,
        items: projects
            .filter(function (proj) { return proj.isMember || isSuperuser; })
            .map(function (proj, index) { return ({
            index: index,
            value: proj.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default project={proj} avatarProps={{ consistentWidth: true }} avatarSize={18} disableLink/>
          </menuItem_1.default>),
            searchKey: proj.slug,
        }); }),
    };
    var projectCrumb = canChangeProject ? projectCrumbDropdown : projectCrumbLink;
    var crumbs = [
        {
            to: "/organizations/" + orgSlug + "/alerts/rules/",
            label: locale_1.t('Alerts'),
            preserveGlobalSelection: true,
        },
        projectCrumb,
        tslib_1.__assign({ label: title }, (alertName
            ? {
                to: "/organizations/" + orgSlug + "/alerts/" + projectSlug + "/wizard",
                preserveGlobalSelection: true,
            }
            : {})),
    ];
    if (alertName) {
        crumbs.push({ label: alertName });
    }
    return <StyledBreadcrumbs crumbs={crumbs}/>;
}
var StyledBreadcrumbs = styled_1.default(breadcrumbs_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 18px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 18px;\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.default = withProjects_1.default(BuilderBreadCrumbs);
var templateObject_1;
//# sourceMappingURL=builderBreadCrumbs.jsx.map