Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchTotalCount = exports.fetchTagFacets = exports.doEventsRequest = void 0;
var tslib_1 = require("tslib");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var utils_1 = require("app/components/charts/utils");
var getPeriod_1 = require("app/utils/getPeriod");
var constants_1 = require("app/utils/performance/constants");
/**
 * Make requests to `events-stats` endpoint
 *
 * @param {Object} api API client instance
 * @param {Object} options Request parameters
 * @param {Object} options.organization Organization object
 * @param {Number[]} options.project List of project ids
 * @param {String[]} options.environment List of environments to query for
 * @param {String[]} options.team List of teams to query for
 * @param {String} options.period Time period to query for, in the format: <integer><units> where units are "d" or "h"
 * @param {String} options.interval Time interval to group results in, in the format: <integer><units> where units are "d", "h", "m", "s"
 * @param {Boolean} options.includePrevious Should request also return reqsults for previous period?
 * @param {Number} options.limit The number of rows to return
 * @param {String} options.query Search query
 */
var doEventsRequest = function (api, _a) {
    var organization = _a.organization, project = _a.project, environment = _a.environment, team = _a.team, period = _a.period, start = _a.start, end = _a.end, interval = _a.interval, includePrevious = _a.includePrevious, query = _a.query, yAxis = _a.yAxis, field = _a.field, topEvents = _a.topEvents, orderby = _a.orderby, partial = _a.partial;
    var shouldDoublePeriod = utils_1.canIncludePreviousPeriod(includePrevious, period);
    var urlQuery = Object.fromEntries(Object.entries({
        interval: interval,
        project: project,
        environment: environment,
        team: team,
        query: query,
        yAxis: yAxis,
        field: field,
        topEvents: topEvents,
        orderby: orderby,
        partial: partial ? '1' : undefined,
    }).filter(function (_a) {
        var _b = tslib_1.__read(_a, 2), value = _b[1];
        return typeof value !== 'undefined';
    }));
    // Doubling period for absolute dates is not accurate unless starting and
    // ending times are the same (at least for daily intervals). This is
    // the tradeoff for now.
    var periodObj = getPeriod_1.getPeriod({ period: period, start: start, end: end }, { shouldDoublePeriod: shouldDoublePeriod });
    return api.requestPromise("/organizations/" + organization.slug + "/events-stats/", {
        query: tslib_1.__assign(tslib_1.__assign({}, urlQuery), periodObj),
    });
};
exports.doEventsRequest = doEventsRequest;
/**
 * Fetches tag facets for a query
 */
function fetchTagFacets(api, orgSlug, query) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var urlParams, queryOption;
        return tslib_1.__generator(this, function (_a) {
            urlParams = pick_1.default(query, Object.values(constants_1.PERFORMANCE_URL_PARAM));
            queryOption = tslib_1.__assign(tslib_1.__assign({}, urlParams), { query: query.query });
            return [2 /*return*/, api.requestPromise("/organizations/" + orgSlug + "/events-facets/", {
                    query: queryOption,
                })];
        });
    });
}
exports.fetchTagFacets = fetchTagFacets;
/**
 * Fetches total count of events for a given query
 */
function fetchTotalCount(api, orgSlug, query) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var urlParams, queryOption;
        return tslib_1.__generator(this, function (_a) {
            urlParams = pick_1.default(query, Object.values(constants_1.PERFORMANCE_URL_PARAM));
            queryOption = tslib_1.__assign(tslib_1.__assign({}, urlParams), { query: query.query });
            return [2 /*return*/, api
                    .requestPromise("/organizations/" + orgSlug + "/events-meta/", {
                    query: queryOption,
                })
                    .then(function (res) { return res.count; })];
        });
    });
}
exports.fetchTotalCount = fetchTotalCount;
//# sourceMappingURL=events.jsx.map