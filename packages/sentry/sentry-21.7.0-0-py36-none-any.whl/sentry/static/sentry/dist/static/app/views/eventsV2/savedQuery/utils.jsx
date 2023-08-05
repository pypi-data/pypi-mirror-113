Object.defineProperty(exports, "__esModule", { value: true });
exports.extractAnalyticsQueryFields = exports.getAnalyticsCreateEventKeyName = exports.handleDeleteQuery = exports.handleUpdateQueryName = exports.handleUpdateQuery = exports.handleCreateQuery = void 0;
var tslib_1 = require("tslib");
var discoverSavedQueries_1 = require("app/actionCreators/discoverSavedQueries");
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
function handleCreateQuery(api, organization, eventView, 
// True if this is a brand new query being saved
// False if this is a modification from a saved query
isNewQuery) {
    if (isNewQuery === void 0) { isNewQuery = true; }
    var payload = eventView.toNewQuery();
    analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'request')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)));
    var promise = discoverSavedQueries_1.createSavedQuery(api, organization.slug, payload);
    promise
        .then(function (savedQuery) {
        indicator_1.addSuccessMessage(locale_1.t('Query saved'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'success')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)));
        return savedQuery;
    })
        .catch(function (err) {
        indicator_1.addErrorMessage(locale_1.t('Query not saved'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'failed')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)), { error: (err && err.message) ||
                "Could not save a " + (isNewQuery ? 'new' : 'existing') + " query" }));
    });
    return promise;
}
exports.handleCreateQuery = handleCreateQuery;
var EVENT_NAME_EXISTING_MAP = {
    request: 'Discoverv2: Request to save a saved query as a new query',
    success: 'Discoverv2: Successfully saved a saved query as a new query',
    failed: 'Discoverv2: Failed to save a saved query as a new query',
};
var EVENT_NAME_NEW_MAP = {
    request: 'Discoverv2: Request to save a new query',
    success: 'Discoverv2: Successfully saved a new query',
    failed: 'Discoverv2: Failed to save a new query',
};
function handleUpdateQuery(api, organization, eventView) {
    var payload = eventView.toNewQuery();
    if (!eventView.name) {
        indicator_1.addErrorMessage(locale_1.t('Please name your query'));
        return Promise.reject();
    }
    analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'discover_v2.update_query_request', eventName: 'Discoverv2: Request to update a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    var promise = discoverSavedQueries_1.updateSavedQuery(api, organization.slug, payload);
    promise
        .then(function (savedQuery) {
        indicator_1.addSuccessMessage(locale_1.t('Query updated'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'discover_v2.update_query_success', eventName: 'Discoverv2: Successfully updated a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
        // NOTE: there is no need to convert _saved into an EventView and push it
        //       to the browser history, since this.props.eventView already
        //       derives from location.
        return savedQuery;
    })
        .catch(function (err) {
        indicator_1.addErrorMessage(locale_1.t('Query not updated'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign({ eventKey: 'discover_v2.update_query_failed', eventName: 'Discoverv2: Failed to update a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)), { error: (err && err.message) || 'Failed to update a query' }));
    });
    return promise;
}
exports.handleUpdateQuery = handleUpdateQuery;
/**
 * Essentially the same as handleUpdateQuery, but specifically for changing the
 * name of the query
 */
function handleUpdateQueryName(api, organization, eventView) {
    var payload = eventView.toNewQuery();
    analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'discover_v2.update_query_name_request', eventName: "Discoverv2: Request to update a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    var promise = discoverSavedQueries_1.updateSavedQuery(api, organization.slug, payload);
    promise
        .then(function (_saved) {
        indicator_1.addSuccessMessage(locale_1.t('Query name saved'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'discover_v2.update_query_name_success', eventName: "Discoverv2: Successfully updated a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    })
        .catch(function (err) {
        indicator_1.addErrorMessage(locale_1.t('Query name not saved'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign({ eventKey: 'discover_v2.update_query_failed', eventName: "Discoverv2: Failed to update a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)), { error: (err && err.message) || 'Failed to update a query name' }));
    });
    return promise;
}
exports.handleUpdateQueryName = handleUpdateQueryName;
function handleDeleteQuery(api, organization, eventView) {
    analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'discover_v2.delete_query_request', eventName: 'Discoverv2: Request to delete a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())));
    var promise = discoverSavedQueries_1.deleteSavedQuery(api, organization.slug, eventView.id);
    promise
        .then(function () {
        indicator_1.addSuccessMessage(locale_1.t('Query deleted'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'discover_v2.delete_query_success', eventName: 'Discoverv2: Successfully deleted a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())));
    })
        .catch(function (err) {
        indicator_1.addErrorMessage(locale_1.t('Query not deleted'));
        analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign({ eventKey: 'discover_v2.delete_query_failed', eventName: 'Discoverv2: Failed to delete a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())), { error: (err && err.message) || 'Failed to delete query' }));
    });
    return promise;
}
exports.handleDeleteQuery = handleDeleteQuery;
function getAnalyticsCreateEventKeyName(
// True if this is a brand new query being saved
// False if this is a modification from a saved query
isNewQuery, type) {
    var eventKey = isNewQuery
        ? 'discover_v2.save_new_query_' + type
        : 'discover_v2.save_existing_query_' + type;
    var eventName = isNewQuery ? EVENT_NAME_NEW_MAP[type] : EVENT_NAME_EXISTING_MAP[type];
    return {
        eventKey: eventKey,
        eventName: eventName,
    };
}
exports.getAnalyticsCreateEventKeyName = getAnalyticsCreateEventKeyName;
/**
 * Takes in a DiscoverV2 NewQuery object and returns a Partial containing
 * the desired fields to populate into reload analytics
 */
function extractAnalyticsQueryFields(payload) {
    var projects = payload.projects, fields = payload.fields, query = payload.query;
    return {
        projects: projects,
        fields: fields,
        query: query,
    };
}
exports.extractAnalyticsQueryFields = extractAnalyticsQueryFields;
//# sourceMappingURL=utils.jsx.map