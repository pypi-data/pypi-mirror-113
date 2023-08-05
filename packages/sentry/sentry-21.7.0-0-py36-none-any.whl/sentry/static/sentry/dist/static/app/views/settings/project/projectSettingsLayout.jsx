Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var AppStoreConnectContext = tslib_1.__importStar(require("app/components/projects/appStoreConnectContext"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var projectContext_1 = tslib_1.__importDefault(require("app/views/projects/projectContext"));
var settingsLayout_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsLayout"));
var projectSettingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/project/projectSettingsNavigation"));
function ProjectSettingsLayout(_a) {
    var params = _a.params, organization = _a.organization, children = _a.children, routes = _a.routes, props = tslib_1.__rest(_a, ["params", "organization", "children", "routes"]);
    var orgId = params.orgId, projectId = params.projectId;
    return (<projectContext_1.default orgId={orgId} projectId={projectId}>
      {function (_a) {
            var project = _a.project;
            return (<AppStoreConnectContext.Provider project={project} organization={organization}>
          <settingsLayout_1.default params={params} routes={routes} {...props} renderNavigation={function () { return (<projectSettingsNavigation_1.default organization={organization}/>); }}>
            {children && React.isValidElement(children)
                    ? React.cloneElement(children, {
                        organization: organization,
                    })
                    : children}
          </settingsLayout_1.default>
        </AppStoreConnectContext.Provider>);
        }}
    </projectContext_1.default>);
}
exports.default = withOrganization_1.default(ProjectSettingsLayout);
//# sourceMappingURL=projectSettingsLayout.jsx.map