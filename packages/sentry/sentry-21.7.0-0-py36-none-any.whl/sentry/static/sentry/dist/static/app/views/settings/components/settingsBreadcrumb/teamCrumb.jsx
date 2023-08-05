Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamCrumb = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var breadcrumbDropdown_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
var menuItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
var _1 = require(".");
var TeamCrumb = function (_a) {
    var teams = _a.teams, params = _a.params, routes = _a.routes, route = _a.route, props = tslib_1.__rest(_a, ["teams", "params", "routes", "route"]);
    var team = teams.find(function (_a) {
        var slug = _a.slug;
        return slug === params.teamId;
    });
    var hasMenu = teams.length > 1;
    if (!team) {
        return null;
    }
    return (<breadcrumbDropdown_1.default name={<_1.CrumbLink to={recreateRoute_1.default(route, {
                routes: routes,
                params: tslib_1.__assign(tslib_1.__assign({}, params), { teamId: team.slug }),
            })}>
          <idBadge_1.default avatarSize={18} team={team}/>
        </_1.CrumbLink>} onSelect={function (item) {
            react_router_1.browserHistory.push(recreateRoute_1.default('', {
                routes: routes,
                params: tslib_1.__assign(tslib_1.__assign({}, params), { teamId: item.value }),
            }));
        }} hasMenu={hasMenu} route={route} items={teams.map(function (teamItem, index) { return ({
            index: index,
            value: teamItem.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default team={teamItem}/>
          </menuItem_1.default>),
        }); })} {...props}/>);
};
exports.TeamCrumb = TeamCrumb;
exports.default = withTeams_1.default(TeamCrumb);
//# sourceMappingURL=teamCrumb.jsx.map