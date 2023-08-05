Object.defineProperty(exports, "__esModule", { value: true });
exports.parseHistogramBucketInfo = exports.tagsRouteWithQuery = exports.trackTagPageInteraction = exports.decodeSelectedTagKey = exports.generateTagsRoute = void 0;
var analytics_1 = require("app/utils/analytics");
var queryString_1 = require("app/utils/queryString");
function generateTagsRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/summary/tags/";
}
exports.generateTagsRoute = generateTagsRoute;
function decodeSelectedTagKey(location) {
    return queryString_1.decodeScalar(location.query.tagKey);
}
exports.decodeSelectedTagKey = decodeSelectedTagKey;
function trackTagPageInteraction(organization) {
    analytics_1.trackAnalyticsEvent({
        eventKey: 'performance_views.tags.interaction',
        eventName: 'Performance Views: Tag Page - Interaction',
        organization_id: parseInt(organization.id, 10),
    });
}
exports.trackTagPageInteraction = trackTagPageInteraction;
function tagsRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query;
    var pathname = generateTagsRoute({
        orgSlug: orgSlug,
    });
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
            tagKey: query.tagKey,
        },
    };
}
exports.tagsRouteWithQuery = tagsRouteWithQuery;
// TODO(k-fish): Improve meta of backend response to return these directly
function parseHistogramBucketInfo(row) {
    var field = Object.keys(row).find(function (f) { return f.includes('histogram'); });
    if (!field) {
        return undefined;
    }
    var parts = field.split('_');
    return {
        histogramField: field,
        bucketSize: parseInt(parts[parts.length - 3], 10),
        offset: parseInt(parts[parts.length - 2], 10),
        multiplier: parseInt(parts[parts.length - 1], 10),
    };
}
exports.parseHistogramBucketInfo = parseHistogramBucketInfo;
//# sourceMappingURL=utils.jsx.map