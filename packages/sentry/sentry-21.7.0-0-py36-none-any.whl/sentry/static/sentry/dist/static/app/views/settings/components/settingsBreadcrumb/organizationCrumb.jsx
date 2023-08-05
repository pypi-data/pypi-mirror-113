Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationCrumb = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var breadcrumbDropdown_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
var findFirstRouteWithoutRouteParam_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/findFirstRouteWithoutRouteParam"));
var menuItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
var _1 = require(".");
var OrganizationCrumb = function (_a) {
    var organization = _a.organization, organizations = _a.organizations, params = _a.params, routes = _a.routes, route = _a.route, props = tslib_1.__rest(_a, ["organization", "organizations", "params", "routes", "route"]);
    var handleSelect = function (item) {
        // If we are currently in a project context, and we're attempting to switch organizations,
        // then we need to default to index route (e.g. `route`)
        //
        // Otherwise, find the last route without a router param
        // e.g. if you are on API details, we want the API listing
        // This fails if our route tree is not nested
        var hasProjectParam = !!params.projectId;
        var destination = hasProjectParam
            ? route
            : findFirstRouteWithoutRouteParam_1.default(routes.slice(routes.indexOf(route)));
        // It's possible there is no route without route params (e.g. organization settings index),
        // in which case, we can use the org settings index route (e.g. `route`)
        if (!hasProjectParam && typeof destination === 'undefined') {
            destination = route;
        }
        if (destination === undefined) {
            return;
        }
        react_router_1.browserHistory.push(recreateRoute_1.default(destination, {
            routes: routes,
            params: tslib_1.__assign(tslib_1.__assign({}, params), { orgId: item.value }),
        }));
    };
    if (!organization) {
        return null;
    }
    var hasMenu = organizations.length > 1;
    return (<breadcrumbDropdown_1.default name={<_1.CrumbLink to={recreateRoute_1.default(route, {
                routes: routes,
                params: tslib_1.__assign(tslib_1.__assign({}, params), { orgId: organization.slug }),
            })}>
          <BadgeWrapper>
            <idBadge_1.default avatarSize={18} organization={organization}/>
          </BadgeWrapper>
        </_1.CrumbLink>} onSelect={handleSelect} hasMenu={hasMenu} route={route} items={organizations.map(function (org, index) { return ({
            index: index,
            value: org.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default organization={org}/>
          </menuItem_1.default>),
        }); })} {...props}/>);
};
exports.OrganizationCrumb = OrganizationCrumb;
var BadgeWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
exports.default = withLatestContext_1.default(OrganizationCrumb);
var templateObject_1;
//# sourceMappingURL=organizationCrumb.jsx.map