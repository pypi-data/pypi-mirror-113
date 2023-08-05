Object.defineProperty(exports, "__esModule", { value: true });
exports.CrumbLink = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var settingsBreadcrumbActions_1 = tslib_1.__importDefault(require("app/actions/settingsBreadcrumbActions"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var settingsBreadcrumbStore_1 = tslib_1.__importDefault(require("app/stores/settingsBreadcrumbStore"));
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var crumb_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/crumb"));
var divider_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/divider"));
var organizationCrumb_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/organizationCrumb"));
var projectCrumb_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/projectCrumb"));
var teamCrumb_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/teamCrumb"));
var MENUS = {
    Organization: organizationCrumb_1.default,
    Project: projectCrumb_1.default,
    Team: teamCrumb_1.default,
};
var SettingsBreadcrumb = /** @class */ (function (_super) {
    tslib_1.__extends(SettingsBreadcrumb, _super);
    function SettingsBreadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsBreadcrumb.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.routes === prevProps.routes) {
            return;
        }
        settingsBreadcrumbActions_1.default.trimMappings(this.props.routes);
    };
    SettingsBreadcrumb.prototype.render = function () {
        var _a = this.props, className = _a.className, routes = _a.routes, params = _a.params, pathMap = _a.pathMap;
        var lastRouteIndex = routes.map(function (r) { return !!r.name; }).lastIndexOf(true);
        return (<Breadcrumbs className={className}>
        {routes.map(function (route, i) {
                if (!route.name) {
                    return null;
                }
                var pathTitle = pathMap[getRouteStringFromRoutes_1.default(routes.slice(0, i + 1))];
                var isLast = i === lastRouteIndex;
                var createMenu = MENUS[route.name];
                var Menu = typeof createMenu === 'function' && createMenu;
                var hasMenu = !!Menu;
                var CrumbPicker = hasMenu
                    ? Menu
                    : function () { return (<crumb_1.default>
                  <CrumbLink to={recreateRoute_1.default(route, { routes: routes, params: params })}>
                    {pathTitle || route.name}{' '}
                  </CrumbLink>
                  <divider_1.default isLast={isLast}/>
                </crumb_1.default>); };
                return (<CrumbPicker key={route.name + ":" + route.path} routes={routes} params={params} route={route} isLast={isLast}/>);
            })}
      </Breadcrumbs>);
    };
    SettingsBreadcrumb.defaultProps = {
        pathMap: {},
    };
    return SettingsBreadcrumb;
}(react_1.Component));
var ConnectedSettingsBreadcrumb = /** @class */ (function (_super) {
    tslib_1.__extends(ConnectedSettingsBreadcrumb, _super);
    function ConnectedSettingsBreadcrumb() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { pathMap: settingsBreadcrumbStore_1.default.getPathMap() };
        _this.unsubscribe = settingsBreadcrumbStore_1.default.listen(function (pathMap) { return _this.setState({ pathMap: pathMap }); }, undefined);
        return _this;
    }
    ConnectedSettingsBreadcrumb.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    ConnectedSettingsBreadcrumb.prototype.render = function () {
        return <SettingsBreadcrumb {...this.props} {...this.state}/>;
    };
    return ConnectedSettingsBreadcrumb;
}(react_1.Component));
exports.default = ConnectedSettingsBreadcrumb;
var CrumbLink = styled_1.default(link_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: block;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: block;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.blue300; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
exports.CrumbLink = CrumbLink;
var Breadcrumbs = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map