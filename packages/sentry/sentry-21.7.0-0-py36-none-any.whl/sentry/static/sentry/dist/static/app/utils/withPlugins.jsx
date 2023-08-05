Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var plugins_1 = require("app/actionCreators/plugins");
var pluginsStore_1 = tslib_1.__importDefault(require("app/stores/pluginsStore"));
var utils_1 = require("app/utils");
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
/**
 * Higher order component that fetches list of plugins and
 * passes PluginsStore to component as `plugins`
 */
function withPlugins(WrappedComponent) {
    var WithPlugins = /** @class */ (function (_super) {
        tslib_1.__extends(WithPlugins, _super);
        function WithPlugins() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { plugins: [], loading: true };
            _this.unsubscribe = pluginsStore_1.default.listen(function (_a) {
                var plugins = _a.plugins, loading = _a.loading;
                // State is destructured as store updates contain additional keys
                // that are not exposed by this HoC
                _this.setState({ plugins: plugins, loading: loading });
            }, undefined);
            return _this;
        }
        WithPlugins.prototype.componentDidMount = function () {
            this.fetchPlugins();
        };
        WithPlugins.prototype.componentDidUpdate = function (prevProps, _prevState, prevContext) {
            var _a = this.props, organization = _a.organization, project = _a.project;
            // Only fetch plugins when a org slug or project slug has changed
            var prevOrg = prevProps.organization || (prevContext === null || prevContext === void 0 ? void 0 : prevContext.organization);
            var prevProject = prevProps.project || (prevContext === null || prevContext === void 0 ? void 0 : prevContext.project);
            // If previous org/project is undefined then it means:
            // the HoC has mounted, `fetchPlugins` has been called (via cDM), and
            // store was updated. We don't need to fetchPlugins again (or it will cause an infinite loop)
            //
            // This is for the unusual case where component is mounted and receives a new org/project prop
            // e.g. when switching projects via breadcrumbs in settings.
            if (!utils_1.defined(prevProject) || !utils_1.defined(prevOrg)) {
                return;
            }
            var isOrgSame = prevOrg.slug === organization.slug;
            var isProjectSame = prevProject.slug === (project === null || project === void 0 ? void 0 : project.slug);
            // Don't do anything if org and project are the same
            if (isOrgSame && isProjectSame) {
                return;
            }
            this.fetchPlugins();
        };
        WithPlugins.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithPlugins.prototype.fetchPlugins = function () {
            var _a = this.props, organization = _a.organization, project = _a.project;
            if (!project || !organization) {
                return;
            }
            plugins_1.fetchPlugins({ projectId: project.slug, orgId: organization.slug });
        };
        WithPlugins.prototype.render = function () {
            return (<WrappedComponent {...this.props} plugins={this.state}/>);
        };
        WithPlugins.displayName = "withPlugins(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithPlugins;
    }(React.Component));
    return withOrganization_1.default(withProject_1.default(WithPlugins));
}
exports.default = withPlugins;
//# sourceMappingURL=withPlugins.jsx.map