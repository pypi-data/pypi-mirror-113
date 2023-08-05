Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteSavedSearch = exports.unpinSearch = exports.pinSearch = exports.fetchRecentSearches = exports.createSavedSearch = exports.saveRecentSearch = exports.fetchProjectSavedSearches = exports.fetchSavedSearches = exports.resetSavedSearches = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var savedSearchesActions_1 = tslib_1.__importDefault(require("app/actions/savedSearchesActions"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var handleXhrErrorResponse_1 = tslib_1.__importDefault(require("app/utils/handleXhrErrorResponse"));
function resetSavedSearches() {
    savedSearchesActions_1.default.resetSavedSearches();
}
exports.resetSavedSearches = resetSavedSearches;
function fetchSavedSearches(api, orgSlug) {
    var url = "/organizations/" + orgSlug + "/searches/";
    savedSearchesActions_1.default.startFetchSavedSearches();
    var promise = api.requestPromise(url, {
        method: 'GET',
    });
    promise
        .then(function (resp) {
        savedSearchesActions_1.default.fetchSavedSearchesSuccess(resp);
    })
        .catch(function (err) {
        savedSearchesActions_1.default.fetchSavedSearchesError(err);
        indicator_1.addErrorMessage(locale_1.t('Unable to load saved searches'));
    });
    return promise;
}
exports.fetchSavedSearches = fetchSavedSearches;
function fetchProjectSavedSearches(api, orgSlug, projectId) {
    var url = "/projects/" + orgSlug + "/" + projectId + "/searches/";
    return api.requestPromise(url, {
        method: 'GET',
    });
}
exports.fetchProjectSavedSearches = fetchProjectSavedSearches;
var getRecentSearchUrl = function (orgSlug) {
    return "/organizations/" + orgSlug + "/recent-searches/";
};
/**
 * Saves search term for `user` + `orgSlug`
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param type Context for where search happened, 0 for issue, 1 for event
 * @param query The search term that was used
 */
function saveRecentSearch(api, orgSlug, type, query) {
    var url = getRecentSearchUrl(orgSlug);
    var promise = api.requestPromise(url, {
        method: 'POST',
        data: {
            query: query,
            type: type,
        },
    });
    promise.catch(handleXhrErrorResponse_1.default('Unable to save a recent search'));
    return promise;
}
exports.saveRecentSearch = saveRecentSearch;
/**
 * Creates a saved search
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param name Saved search name
 * @param query Query to save
 */
function createSavedSearch(api, orgSlug, name, query, sort) {
    var promise = api.requestPromise("/organizations/" + orgSlug + "/searches/", {
        method: 'POST',
        data: {
            type: types_1.SavedSearchType.ISSUE,
            query: query,
            name: name,
            sort: sort,
        },
    });
    // Need to wait for saved search to save unfortunately because we need to redirect
    // to saved search URL
    promise.then(function (resp) {
        savedSearchesActions_1.default.createSavedSearchSuccess(resp);
    });
    return promise;
}
exports.createSavedSearch = createSavedSearch;
/**
 * Fetches a list of recent search terms conducted by `user` for `orgSlug`
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param type Context for where search happened, 0 for issue, 1 for event
 * @param query A query term used to filter results
 *
 * @return Returns a list of objects of recent search queries performed by user
 */
function fetchRecentSearches(api, orgSlug, type, query) {
    var url = getRecentSearchUrl(orgSlug);
    var promise = api.requestPromise(url, {
        query: {
            query: query,
            type: type,
            limit: constants_1.MAX_AUTOCOMPLETE_RECENT_SEARCHES,
        },
    });
    promise.catch(function (resp) {
        if (resp.status !== 401 && resp.status !== 403) {
            handleXhrErrorResponse_1.default('Unable to fetch recent searches')(resp);
        }
    });
    return promise;
}
exports.fetchRecentSearches = fetchRecentSearches;
var getPinSearchUrl = function (orgSlug) {
    return "/organizations/" + orgSlug + "/pinned-searches/";
};
function pinSearch(api, orgSlug, type, query, sort) {
    var url = getPinSearchUrl(orgSlug);
    // Optimistically update store
    savedSearchesActions_1.default.pinSearch(type, query, sort);
    var promise = api.requestPromise(url, {
        method: 'PUT',
        data: {
            query: query,
            type: type,
            sort: sort,
        },
    });
    promise.then(savedSearchesActions_1.default.pinSearchSuccess);
    promise.catch(handleXhrErrorResponse_1.default('Unable to pin search'));
    promise.catch(function () {
        savedSearchesActions_1.default.unpinSearch(type);
    });
    return promise;
}
exports.pinSearch = pinSearch;
function unpinSearch(api, orgSlug, type, pinnedSearch) {
    var url = getPinSearchUrl(orgSlug);
    // Optimistically update store
    savedSearchesActions_1.default.unpinSearch(type);
    var promise = api.requestPromise(url, {
        method: 'DELETE',
        data: {
            type: type,
        },
    });
    promise.catch(handleXhrErrorResponse_1.default('Unable to un-pin search'));
    promise.catch(function () {
        var pinnedType = pinnedSearch.type, query = pinnedSearch.query;
        savedSearchesActions_1.default.pinSearch(pinnedType, query);
    });
    return promise;
}
exports.unpinSearch = unpinSearch;
/**
 * Send a DELETE request to remove a saved search
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param search The search to remove.
 */
function deleteSavedSearch(api, orgSlug, search) {
    var url = "/organizations/" + orgSlug + "/searches/" + search.id + "/";
    var promise = api
        .requestPromise(url, {
        method: 'DELETE',
    })
        .then(function () { return savedSearchesActions_1.default.deleteSavedSearchSuccess(search); })
        .catch(handleXhrErrorResponse_1.default('Unable to delete a saved search'));
    return promise;
}
exports.deleteSavedSearch = deleteSavedSearch;
//# sourceMappingURL=savedSearches.jsx.map