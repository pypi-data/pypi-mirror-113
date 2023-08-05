Object.defineProperty(exports, "__esModule", { value: true });
exports.eventViewFromWidget = exports.cloneDashboard = void 0;
var tslib_1 = require("tslib");
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var dates_1 = require("app/utils/dates");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
function cloneDashboard(dashboard) {
    return cloneDeep_1.default(dashboard);
}
exports.cloneDashboard = cloneDashboard;
function eventViewFromWidget(title, query, selection) {
    var _a = selection.datetime, start = _a.start, end = _a.end, statsPeriod = _a.period;
    var projects = selection.projects, environments = selection.environments;
    return eventView_1.default.fromSavedQuery({
        id: undefined,
        name: title,
        version: 2,
        fields: query.fields,
        query: query.conditions,
        orderby: query.orderby,
        projects: projects,
        range: statsPeriod,
        start: start ? dates_1.getUtcDateString(start) : undefined,
        end: end ? dates_1.getUtcDateString(end) : undefined,
        environment: environments,
    });
}
exports.eventViewFromWidget = eventViewFromWidget;
//# sourceMappingURL=utils.jsx.map