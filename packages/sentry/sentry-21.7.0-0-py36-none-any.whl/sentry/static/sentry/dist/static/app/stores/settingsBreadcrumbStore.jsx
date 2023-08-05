Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var settingsBreadcrumbActions_1 = tslib_1.__importDefault(require("app/actions/settingsBreadcrumbActions"));
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var storeConfig = {
    pathMap: {},
    init: function () {
        this.reset();
        this.listenTo(settingsBreadcrumbActions_1.default.mapTitle, this.onUpdateRouteMap);
        this.listenTo(settingsBreadcrumbActions_1.default.trimMappings, this.onTrimMappings);
    },
    reset: function () {
        this.pathMap = {};
    },
    getPathMap: function () {
        return this.pathMap;
    },
    onUpdateRouteMap: function (_a) {
        var routes = _a.routes, title = _a.title;
        this.pathMap[getRouteStringFromRoutes_1.default(routes)] = title;
        this.trigger(this.pathMap);
    },
    onTrimMappings: function (routes) {
        var routePath = getRouteStringFromRoutes_1.default(routes);
        for (var fullPath in this.pathMap) {
            if (!routePath.startsWith(fullPath)) {
                delete this.pathMap[fullPath];
            }
        }
        this.trigger(this.pathMap);
    },
};
var SettingsBreadcrumbStore = reflux_1.default.createStore(storeConfig);
exports.default = SettingsBreadcrumbStore;
//# sourceMappingURL=settingsBreadcrumbStore.jsx.map