Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationRoot = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var navigation_1 = require("app/actionCreators/navigation");
var projects_1 = require("app/actionCreators/projects");
/**
 * This is the parent container for organization-level views such
 * as the Dashboard, Stats, Activity, etc...
 *
 * Currently is just used to unset active project
 */
var OrganizationRoot = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationRoot, _super);
    function OrganizationRoot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationRoot.prototype.componentDidMount = function () {
        projects_1.setActiveProject(null);
    };
    OrganizationRoot.prototype.componentWillUnmount = function () {
        var location = this.props.location;
        var pathname = location.pathname, search = location.search;
        // Save last route so that we can jump back to view from settings
        navigation_1.setLastRoute("" + pathname + (search || ''));
    };
    OrganizationRoot.prototype.render = function () {
        return this.props.children;
    };
    return OrganizationRoot;
}(react_1.Component));
exports.OrganizationRoot = OrganizationRoot;
exports.default = react_router_1.withRouter(OrganizationRoot);
//# sourceMappingURL=organizationRoot.jsx.map