var _a, _b;
Object.defineProperty(exports, "__esModule", { value: true });
exports.getQueryDatasource = exports.convertDatasetEventTypesToSource = exports.DATA_SOURCE_TO_SET_AND_EVENT_TYPES = exports.DATA_SOURCE_LABELS = exports.isIssueAlert = exports.getIncidentDiscoverUrl = exports.getStartEndFromStats = exports.getIncidentMetricPreset = exports.isOpen = exports.updateStatus = exports.updateSubscription = exports.fetchIncidentStats = exports.fetchIncident = exports.fetchIncidentsForRule = exports.fetchAlertRule = void 0;
var tslib_1 = require("tslib");
var api_1 = require("app/api");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var presets_1 = require("app/views/alerts/incidentRules/presets");
var types_1 = require("app/views/alerts/incidentRules/types");
var types_2 = require("../types");
// Use this api for requests that are getting cancelled
var uncancellableApi = new api_1.Client();
function fetchAlertRule(orgId, ruleId) {
    return uncancellableApi.requestPromise("/organizations/" + orgId + "/alert-rules/" + ruleId + "/");
}
exports.fetchAlertRule = fetchAlertRule;
function fetchIncidentsForRule(orgId, alertRule, start, end) {
    return uncancellableApi.requestPromise("/organizations/" + orgId + "/incidents/", {
        query: {
            alertRule: alertRule,
            includeSnapshots: true,
            start: start,
            end: end,
            expand: ['activities', 'seen_by', 'original_alert_rule'],
        },
    });
}
exports.fetchIncidentsForRule = fetchIncidentsForRule;
function fetchIncident(api, orgId, alertId) {
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/");
}
exports.fetchIncident = fetchIncident;
function fetchIncidentStats(api, orgId, alertId) {
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/stats/");
}
exports.fetchIncidentStats = fetchIncidentStats;
function updateSubscription(api, orgId, alertId, isSubscribed) {
    var method = isSubscribed ? 'POST' : 'DELETE';
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/subscriptions/", {
        method: method,
    });
}
exports.updateSubscription = updateSubscription;
function updateStatus(api, orgId, alertId, status) {
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/", {
        method: 'PUT',
        data: {
            status: status,
        },
    });
}
exports.updateStatus = updateStatus;
/**
 * Is incident open?
 *
 * @param {Object} incident Incident object
 * @returns {Boolean}
 */
function isOpen(incident) {
    switch (incident.status) {
        case types_2.IncidentStatus.CLOSED:
            return false;
        default:
            return true;
    }
}
exports.isOpen = isOpen;
function getIncidentMetricPreset(incident) {
    var _a, _b;
    var alertRule = incident === null || incident === void 0 ? void 0 : incident.alertRule;
    var aggregate = (_a = alertRule === null || alertRule === void 0 ? void 0 : alertRule.aggregate) !== null && _a !== void 0 ? _a : '';
    var dataset = (_b = alertRule === null || alertRule === void 0 ? void 0 : alertRule.dataset) !== null && _b !== void 0 ? _b : types_1.Dataset.ERRORS;
    return presets_1.PRESET_AGGREGATES.find(function (p) { return p.validDataset.includes(dataset) && p.match.test(aggregate); });
}
exports.getIncidentMetricPreset = getIncidentMetricPreset;
/**
 * Gets start and end date query parameters from stats
 */
function getStartEndFromStats(stats) {
    var start = dates_1.getUtcDateString(stats.eventStats.data[0][0] * 1000);
    var end = dates_1.getUtcDateString(stats.eventStats.data[stats.eventStats.data.length - 1][0] * 1000);
    return { start: start, end: end };
}
exports.getStartEndFromStats = getStartEndFromStats;
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
    var _b = getStartEndFromStats(stats), start = _b.start, end = _b.end;
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
function isIssueAlert(data) {
    return !data.hasOwnProperty('triggers');
}
exports.isIssueAlert = isIssueAlert;
exports.DATA_SOURCE_LABELS = (_a = {},
    _a[types_1.Dataset.ERRORS] = locale_1.t('Errors'),
    _a[types_1.Dataset.TRANSACTIONS] = locale_1.t('Transactions'),
    _a[types_1.Datasource.ERROR_DEFAULT] = locale_1.t('event.type:error OR event.type:default'),
    _a[types_1.Datasource.ERROR] = locale_1.t('event.type:error'),
    _a[types_1.Datasource.DEFAULT] = locale_1.t('event.type:default'),
    _a[types_1.Datasource.TRANSACTION] = locale_1.t('event.type:transaction'),
    _a);
// Maps a datasource to the relevant dataset and event_types for the backend to use
exports.DATA_SOURCE_TO_SET_AND_EVENT_TYPES = (_b = {},
    _b[types_1.Datasource.ERROR_DEFAULT] = {
        dataset: types_1.Dataset.ERRORS,
        eventTypes: [types_1.EventTypes.ERROR, types_1.EventTypes.DEFAULT],
    },
    _b[types_1.Datasource.ERROR] = {
        dataset: types_1.Dataset.ERRORS,
        eventTypes: [types_1.EventTypes.ERROR],
    },
    _b[types_1.Datasource.DEFAULT] = {
        dataset: types_1.Dataset.ERRORS,
        eventTypes: [types_1.EventTypes.DEFAULT],
    },
    _b[types_1.Datasource.TRANSACTION] = {
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: [types_1.EventTypes.TRANSACTION],
    },
    _b);
// Converts the given dataset and event types array to a datasource for the datasource dropdown
function convertDatasetEventTypesToSource(dataset, eventTypes) {
    // transactions only has one datasource option regardless of event type
    if (dataset === types_1.Dataset.TRANSACTIONS) {
        return types_1.Datasource.TRANSACTION;
    }
    // if no event type was provided use the default datasource
    if (!eventTypes) {
        return types_1.Datasource.ERROR;
    }
    if (eventTypes.includes(types_1.EventTypes.DEFAULT) && eventTypes.includes(types_1.EventTypes.ERROR)) {
        return types_1.Datasource.ERROR_DEFAULT;
    }
    else if (eventTypes.includes(types_1.EventTypes.DEFAULT)) {
        return types_1.Datasource.DEFAULT;
    }
    else {
        return types_1.Datasource.ERROR;
    }
}
exports.convertDatasetEventTypesToSource = convertDatasetEventTypesToSource;
/**
 * Attempt to guess the data source of a discover query
 *
 * @returns An object containing the datasource and new query without the datasource.
 * Returns null on no datasource.
 */
function getQueryDatasource(query) {
    var match = query.match(/\(?\bevent\.type:(error|default|transaction)\)?\WOR\W\(?event\.type:(error|default|transaction)\)?/i);
    if (match) {
        // should be [error, default] or [default, error]
        var eventTypes = match.slice(1, 3).sort().join(',');
        if (eventTypes !== 'default,error') {
            return null;
        }
        return { source: types_1.Datasource.ERROR_DEFAULT, query: query.replace(match[0], '').trim() };
    }
    match = query.match(/(^|\s)event\.type:(error|default|transaction)/i);
    if (match && types_1.Datasource[match[2].toUpperCase()]) {
        return {
            source: types_1.Datasource[match[2].toUpperCase()],
            query: query.replace(match[0], '').trim(),
        };
    }
    return null;
}
exports.getQueryDatasource = getQueryDatasource;
//# sourceMappingURL=index.jsx.map