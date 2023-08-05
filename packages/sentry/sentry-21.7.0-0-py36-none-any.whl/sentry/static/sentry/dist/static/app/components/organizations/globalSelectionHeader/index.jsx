Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjectsSpecified_1 = tslib_1.__importDefault(require("app/utils/withProjectsSpecified"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("./globalSelectionHeader"));
var initializeGlobalSelectionHeader_1 = tslib_1.__importDefault(require("./initializeGlobalSelectionHeader"));
var GlobalSelectionHeaderContainer = /** @class */ (function (_super) {
    tslib_1.__extends(GlobalSelectionHeaderContainer, _super);
    function GlobalSelectionHeaderContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getProjects = function () {
            var _a = _this.props, organization = _a.organization, projects = _a.projects;
            var isSuperuser = configStore_1.default.get('user').isSuperuser;
            var isOrgAdmin = organization.access.includes('org:admin');
            var _b = tslib_1.__read(partition_1.default(projects, function (project) { return project.isMember; }), 2), memberProjects = _b[0], nonMemberProjects = _b[1];
            if (isSuperuser || isOrgAdmin) {
                return [memberProjects, nonMemberProjects];
            }
            return [memberProjects, []];
        };
        return _this;
    }
    GlobalSelectionHeaderContainer.prototype.render = function () {
        var _a = this.props, loadingProjects = _a.loadingProjects, location = _a.location, organization = _a.organization, router = _a.router, routes = _a.routes, defaultSelection = _a.defaultSelection, forceProject = _a.forceProject, shouldForceProject = _a.shouldForceProject, skipLoadLastUsed = _a.skipLoadLastUsed, showAbsolute = _a.showAbsolute, props = tslib_1.__rest(_a, ["loadingProjects", "location", "organization", "router", "routes", "defaultSelection", "forceProject", "shouldForceProject", "skipLoadLastUsed", "showAbsolute"]);
        var enforceSingleProject = !organization.features.includes('global-views');
        var _b = tslib_1.__read(this.getProjects(), 2), memberProjects = _b[0], nonMemberProjects = _b[1];
        // We can initialize before ProjectsStore is fully loaded if we don't need to enforce single project.
        return (<React.Fragment>
        {(!loadingProjects || (!shouldForceProject && !enforceSingleProject)) && (<initializeGlobalSelectionHeader_1.default location={location} skipLoadLastUsed={!!skipLoadLastUsed} router={router} organization={organization} defaultSelection={defaultSelection} forceProject={forceProject} shouldForceProject={!!shouldForceProject} shouldEnforceSingleProject={enforceSingleProject} memberProjects={memberProjects} showAbsolute={showAbsolute}/>)}
        <globalSelectionHeader_1.default {...props} loadingProjects={loadingProjects} location={location} organization={organization} router={router} routes={routes} shouldForceProject={!!shouldForceProject} defaultSelection={defaultSelection} forceProject={forceProject} memberProjects={memberProjects} nonMemberProjects={nonMemberProjects} showAbsolute={showAbsolute}/>
      </React.Fragment>);
    };
    return GlobalSelectionHeaderContainer;
}(React.Component));
exports.default = withOrganization_1.default(withProjectsSpecified_1.default(ReactRouter.withRouter(GlobalSelectionHeaderContainer)));
//# sourceMappingURL=index.jsx.map