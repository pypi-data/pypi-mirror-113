Object.defineProperty(exports, "__esModule", { value: true });
exports.getIncidentDiscoverUrl = void 0;
var tslib_1 = require("tslib");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var types_1 = require("app/views/alerts/incidentRules/types");
var utils_1 = require("app/views/alerts/utils");
/**
 * Gets the URL for a discover view of the incident with the following default
 * parameters:
 *
 * - Ordered by the incident aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alerts: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alerts: [transaction, count()]
 * - Start and end are scoped to the same period as the alert rule
 */
function getIncidentDiscoverUrl(opts) {
    var _a;
    var orgSlug = opts.orgSlug, projects = opts.projects, incident = opts.incident, stats = opts.stats, extraQueryParams = opts.extraQueryParams;
    if (!projects || !projects.length || !incident || !stats) {
        return '';
    }
    var timeWindowString = incident.alertRule.timeWindow + "m";
    var _b = utils_1.getStartEndFromStats(stats), start = _b.start, end = _b.end;
    var discoverQuery = tslib_1.__assign({ id: undefined, name: (incident && incident.title) || '', orderby: "-" + fields_1.getAggregateAlias(incident.alertRule.aggregate), yAxis: incident.alertRule.aggregate, query: (_a = incident === null || incident === void 0 ? void 0 : incident.discoverQuery) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(function (_a) {
            var slug = _a.slug;
            return incident.projects.includes(slug);
        })
            .map(function (_a) {
            var id = _a.id;
            return Number(id);
        }), version: 2, fields: incident.alertRule.dataset === types_1.Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', incident.alertRule.aggregate], start: start, end: end }, extraQueryParams);
    var discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
    var _c = discoverView.getResultsViewUrlTarget(orgSlug), query = _c.query, toObject = tslib_1.__rest(_c, ["query"]);
    return tslib_1.__assign({ query: tslib_1.__assign(tslib_1.__assign({}, query), { interval: timeWindowString }) }, toObject);
}
exports.getIncidentDiscoverUrl = getIncidentDiscoverUrl;
//# sourceMappingURL=getIncidentDiscoverUrl.jsx.map