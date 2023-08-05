Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchTagValues = exports.fetchOrganizationTags = exports.loadOrganizationTags = void 0;
var tslib_1 = require("tslib");
var alertActions_1 = tslib_1.__importDefault(require("app/actions/alertActions"));
var tagActions_1 = tslib_1.__importDefault(require("app/actions/tagActions"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var locale_1 = require("app/locale");
var tagStore_1 = tslib_1.__importDefault(require("app/stores/tagStore"));
var MAX_TAGS = 1000;
function tagFetchSuccess(tags) {
    // We occasionally get undefined passed in when APIs are having a bad time.
    tags = tags || [];
    var trimmedTags = tags.slice(0, MAX_TAGS);
    if (tags.length > MAX_TAGS) {
        alertActions_1.default.addAlert({
            message: locale_1.t('You have too many unique tags and some have been truncated'),
            type: 'warn',
        });
    }
    tagActions_1.default.loadTagsSuccess(trimmedTags);
}
/**
 * Load an organization's tags based on a global selection value.
 */
function loadOrganizationTags(api, orgId, selection) {
    tagStore_1.default.reset();
    var url = "/organizations/" + orgId + "/tags/";
    var query = selection.datetime ? tslib_1.__assign({}, getParams_1.getParams(selection.datetime)) : {};
    query.use_cache = '1';
    if (selection.projects) {
        query.project = selection.projects.map(String);
    }
    var promise = api.requestPromise(url, {
        method: 'GET',
        query: query,
    });
    promise.then(tagFetchSuccess, tagActions_1.default.loadTagsError);
    return promise;
}
exports.loadOrganizationTags = loadOrganizationTags;
/**
 * Fetch tags for an organization or a subset or projects.
 */
function fetchOrganizationTags(api, orgId, projectIds) {
    if (projectIds === void 0) { projectIds = null; }
    tagStore_1.default.reset();
    var url = "/organizations/" + orgId + "/tags/";
    var query = { use_cache: '1' };
    if (projectIds) {
        query.project = projectIds;
    }
    var promise = api.requestPromise(url, {
        method: 'GET',
        query: query,
    });
    promise.then(tagFetchSuccess, tagActions_1.default.loadTagsError);
    return promise;
}
exports.fetchOrganizationTags = fetchOrganizationTags;
/**
 * Fetch tag values for an organization.
 * The `projectIds` argument can be used to subset projects.
 */
function fetchTagValues(api, orgId, tagKey, search, projectIds, endpointParams, includeTransactions) {
    if (search === void 0) { search = null; }
    if (projectIds === void 0) { projectIds = null; }
    if (endpointParams === void 0) { endpointParams = null; }
    if (includeTransactions === void 0) { includeTransactions = false; }
    var url = "/organizations/" + orgId + "/tags/" + tagKey + "/values/";
    var query = {};
    if (search) {
        query.query = search;
    }
    if (projectIds) {
        query.project = projectIds;
    }
    if (endpointParams) {
        if (endpointParams.start) {
            query.start = endpointParams.start;
        }
        if (endpointParams.end) {
            query.end = endpointParams.end;
        }
        if (endpointParams.statsPeriod) {
            query.statsPeriod = endpointParams.statsPeriod;
        }
    }
    if (includeTransactions) {
        query.includeTransactions = '1';
    }
    return api.requestPromise(url, {
        method: 'GET',
        query: query,
    });
}
exports.fetchTagValues = fetchTagValues;
//# sourceMappingURL=tags.jsx.map