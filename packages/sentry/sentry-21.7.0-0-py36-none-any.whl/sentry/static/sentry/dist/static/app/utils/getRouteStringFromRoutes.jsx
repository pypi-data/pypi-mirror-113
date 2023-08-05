Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var findLastIndex_1 = tslib_1.__importDefault(require("lodash/findLastIndex"));
/**
 * Creates a route string from an array of `routes` from react-router
 *
 * It will look for the last route path that begins with a `/` and
 * concatenate all of the following routes. Skips any routes without a path
 *
 * @param {Array<{}>} routes An array of route objects from react-router
 * @return String Returns a route path
 */
function getRouteStringFromRoutes(routes) {
    if (!Array.isArray(routes)) {
        return '';
    }
    var routesWithPaths = routes.filter(function (route) { return !!route.path; });
    var lastAbsolutePathIndex = findLastIndex_1.default(routesWithPaths, function (_a) {
        var path = _a.path;
        return path.startsWith('/');
    });
    return routesWithPaths
        .slice(lastAbsolutePathIndex)
        .filter(function (_a) {
        var path = _a.path;
        return !!path;
    })
        .map(function (_a) {
        var path = _a.path;
        return path;
    })
        .join('');
}
exports.default = getRouteStringFromRoutes;
//# sourceMappingURL=getRouteStringFromRoutes.jsx.map