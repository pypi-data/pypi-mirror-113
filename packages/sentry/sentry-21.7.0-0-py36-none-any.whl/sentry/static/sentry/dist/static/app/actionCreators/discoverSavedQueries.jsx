Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteSavedQuery = exports.updateSavedQuery = exports.createSavedQuery = exports.fetchSavedQuery = exports.fetchSavedQueries = void 0;
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
function fetchSavedQueries(api, orgId, query) {
    if (query === void 0) { query = ''; }
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/", {
        method: 'GET',
        query: { query: ("version:2 " + query).trim() },
    });
    promise.catch(function () {
        indicator_1.addErrorMessage(locale_1.t('Unable to load saved queries'));
    });
    return promise;
}
exports.fetchSavedQueries = fetchSavedQueries;
function fetchSavedQuery(api, orgId, queryId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/" + queryId + "/", {
        method: 'GET',
    });
    promise.catch(function () {
        indicator_1.addErrorMessage(locale_1.t('Unable to load saved query'));
    });
    return promise;
}
exports.fetchSavedQuery = fetchSavedQuery;
function createSavedQuery(api, orgId, query) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/", {
        method: 'POST',
        data: query,
    });
    promise.catch(function () {
        indicator_1.addErrorMessage(locale_1.t('Unable to create your saved query'));
    });
    return promise;
}
exports.createSavedQuery = createSavedQuery;
function updateSavedQuery(api, orgId, query) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/" + query.id + "/", {
        method: 'PUT',
        data: query,
    });
    promise.catch(function () {
        indicator_1.addErrorMessage(locale_1.t('Unable to update your saved query'));
    });
    return promise;
}
exports.updateSavedQuery = updateSavedQuery;
function deleteSavedQuery(api, orgId, queryId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/" + queryId + "/", { method: 'DELETE' });
    promise.catch(function () {
        indicator_1.addErrorMessage(locale_1.t('Unable to delete the saved query'));
    });
    return promise;
}
exports.deleteSavedQuery = deleteSavedQuery;
//# sourceMappingURL=discoverSavedQueries.jsx.map