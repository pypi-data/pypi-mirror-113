Object.defineProperty(exports, "__esModule", { value: true });
exports.getIncidentRuleDiscoverUrl = void 0;
var tslib_1 = require("tslib");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var types_1 = require("app/views/alerts/incidentRules/types");
/**
 * Gets the URL for a discover view of the rule with the following default
 * parameters:
 *
 * - Ordered by the rule aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alert rules: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alert rules: [transaction, count()]
 * - Start and end are the period's values selected in the chart header
 */
function getIncidentRuleDiscoverUrl(opts) {
    var _a;
    var orgSlug = opts.orgSlug, projects = opts.projects, rule = opts.rule, eventType = opts.eventType, start = opts.start, end = opts.end, extraQueryParams = opts.extraQueryParams;
    var eventTypeTagFilter = eventType && (rule === null || rule === void 0 ? void 0 : rule.query) ? eventType : '';
    if (!projects || !projects.length || !rule || (!start && !end)) {
        return '';
    }
    var timeWindowString = rule.timeWindow + "m";
    var discoverQuery = tslib_1.__assign({ id: undefined, name: (rule && rule.name) || '', orderby: "-" + fields_1.getAggregateAlias(rule.aggregate), yAxis: rule.aggregate, query: (_a = (eventTypeTagFilter || (rule === null || rule === void 0 ? void 0 : rule.query) || eventType)) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(function (_a) {
            var slug = _a.slug;
            return rule.projects.includes(slug);
        })
            .map(function (_a) {
            var id = _a.id;
            return Number(id);
        }), version: 2, fields: rule.dataset === types_1.Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', rule.aggregate], start: start, end: end }, extraQueryParams);
    var discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
    var _b = discoverView.getResultsViewUrlTarget(orgSlug), query = _b.query, toObject = tslib_1.__rest(_b, ["query"]);
    return tslib_1.__assign({ query: tslib_1.__assign(tslib_1.__assign({}, query), { interval: timeWindowString }) }, toObject);
}
exports.getIncidentRuleDiscoverUrl = getIncidentRuleDiscoverUrl;
//# sourceMappingURL=getIncidentRuleDiscoverUrl.jsx.map