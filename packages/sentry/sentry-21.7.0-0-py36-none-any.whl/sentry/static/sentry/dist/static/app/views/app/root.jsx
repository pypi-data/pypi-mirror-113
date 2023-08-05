Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var constants_1 = require("app/constants");
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
/**
 * This view is used when a user lands on the route `/` which historically
 * is a server-rendered route which redirects the user to their last selected organization
 *
 * However, this does not work when in the experimental SPA mode (e.g. developing against a remote API,
 * or a deploy preview), so we must replicate the functionality and redirect
 * the user to the proper organization.
 *
 * TODO: There might be an edge case where user does not have `lastOrganization` set,
 * in which case we should load their list of organizations and make a decision
 */
var AppRoot = /** @class */ (function (_super) {
    tslib_1.__extends(AppRoot, _super);
    function AppRoot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AppRoot.prototype.componentDidMount = function () {
        var config = this.props.config;
        if (config.lastOrganization) {
            react_router_1.browserHistory.replace(replaceRouterParams_1.default(constants_1.DEFAULT_APP_ROUTE, { orgSlug: config.lastOrganization }));
        }
    };
    AppRoot.prototype.render = function () {
        return null;
    };
    return AppRoot;
}(react_1.Component));
exports.default = withConfig_1.default(AppRoot);
//# sourceMappingURL=root.jsx.map