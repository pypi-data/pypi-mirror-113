Object.defineProperty(exports, "__esModule", { value: true });
exports.trackAdvancedAnalyticsEvent = exports.getAnalyticsSessionId = exports.clearAnalyticsSession = exports.startAnalyticsSession = void 0;
var tslib_1 = require("tslib");
var qs = tslib_1.__importStar(require("query-string"));
var analytics_1 = require("app/utils/analytics");
var growthAnalyticsEvents_1 = require("app/utils/growthAnalyticsEvents");
var guid_1 = require("app/utils/guid");
var integrationEvents_1 = require("app/utils/integrationEvents");
var ANALYTICS_SESSION = 'ANALYTICS_SESSION';
var startAnalyticsSession = function () {
    var sessionId = guid_1.uniqueId();
    window.sessionStorage.setItem(ANALYTICS_SESSION, sessionId);
    return sessionId;
};
exports.startAnalyticsSession = startAnalyticsSession;
var clearAnalyticsSession = function () {
    window.sessionStorage.removeItem(ANALYTICS_SESSION);
};
exports.clearAnalyticsSession = clearAnalyticsSession;
var getAnalyticsSessionId = function () {
    return window.sessionStorage.getItem(ANALYTICS_SESSION);
};
exports.getAnalyticsSessionId = getAnalyticsSessionId;
var hasAnalyticsDebug = function () { return window.localStorage.getItem('DEBUG_ANALYTICS') === '1'; };
var allEventMap = tslib_1.__assign(tslib_1.__assign({}, integrationEvents_1.integrationEventMap), growthAnalyticsEvents_1.growthEventMap);
/**
 * Tracks an event for analytics.
 * Must be tied to an organization.
 * Uses the current session ID or generates a new one if startSession == true.
 * An analytics session corresponds to a single action funnel such as installation.
 * Tracking by session allows us to track individual funnel attempts for a single user.
 */
function trackAdvancedAnalyticsEvent(eventKey, analyticsParams, org, // if org is undefined, event won't be recorded
options, mapValuesFn) {
    try {
        var startSession = (options || {}).startSession;
        var sessionId = startSession ? exports.startAnalyticsSession() : exports.getAnalyticsSessionId();
        var eventName = allEventMap[eventKey];
        // we should always have a session id but if we don't, we should generate one
        if (hasAnalyticsDebug() && !sessionId) {
            // eslint-disable-next-line no-console
            console.warn("analytics_session_id absent from event " + eventKey);
            sessionId = exports.startAnalyticsSession();
        }
        var custom_referrer = void 0;
        try {
            // pull the referrer from the query parameter of the page
            var referrer = (qs.parse(window.location.search) || {}).referrer;
            if (typeof referrer === 'string') {
                // Amplitude has its own referrer which inteferes with our custom referrer
                custom_referrer = referrer;
            }
        }
        catch (_a) {
            // ignore if this fails to parse
            // this can happen if we have an invalid query string
            // e.g. unencoded "%"
        }
        // if org is null, we want organization_id to be null
        var organization_id = org ? org.id : org;
        var params = tslib_1.__assign({ eventKey: eventKey, eventName: eventName, analytics_session_id: sessionId, organization_id: organization_id, role: org === null || org === void 0 ? void 0 : org.role, custom_referrer: custom_referrer }, analyticsParams);
        if (mapValuesFn) {
            params = mapValuesFn(params);
        }
        // could put this into a debug method or for the main trackAnalyticsEvent event
        if (hasAnalyticsDebug()) {
            // eslint-disable-next-line no-console
            console.log('trackAdvancedAnalytics', params);
        }
        analytics_1.trackAnalyticsEvent(params);
    }
    catch (e) {
        // eslint-disable-next-line no-console
        console.error('Error tracking analytics event', e);
    }
}
exports.trackAdvancedAnalyticsEvent = trackAdvancedAnalyticsEvent;
//# sourceMappingURL=advancedAnalytics.jsx.map