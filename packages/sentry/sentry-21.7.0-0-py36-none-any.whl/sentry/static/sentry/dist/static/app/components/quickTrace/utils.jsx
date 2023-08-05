Object.defineProperty(exports, "__esModule", { value: true });
exports.generateTraceTarget = exports.generateMultiTransactionsTarget = exports.generateSingleTransactionTarget = exports.generateSingleErrorTarget = exports.generateIssueEventTarget = exports.isQuickTraceEvent = void 0;
var tslib_1 = require("tslib");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var utils_1 = require("app/utils");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var urls_1 = require("app/utils/discover/urls");
var utils_2 = require("app/utils/performance/quickTrace/utils");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_3 = require("app/views/performance/traceDetails/utils");
var utils_4 = require("app/views/performance/utils");
function isQuickTraceEvent(event) {
    return utils_1.defined(event['transaction.duration']);
}
exports.isQuickTraceEvent = isQuickTraceEvent;
function generateIssueEventTarget(event, organization) {
    return "/organizations/" + organization.slug + "/issues/" + event.issue_id + "/events/" + event.event_id;
}
exports.generateIssueEventTarget = generateIssueEventTarget;
function generatePerformanceEventTarget(event, organization, location) {
    var eventSlug = urls_1.generateEventSlug({
        id: event.event_id,
        project: event.project_slug,
    });
    return utils_4.getTransactionDetailsUrl(organization, eventSlug, event.transaction, location.query);
}
function generateDiscoverEventTarget(event, organization, location) {
    var eventSlug = urls_1.generateEventSlug({
        id: event.event_id,
        project: event.project_slug,
    });
    return urls_1.eventDetailsRouteWithEventView({
        orgSlug: organization.slug,
        eventSlug: eventSlug,
        eventView: eventView_1.default.fromLocation(location),
    });
}
function generateSingleErrorTarget(event, organization, location, destination) {
    switch (destination) {
        case 'issue':
            return generateIssueEventTarget(event, organization);
        case 'discover':
        default:
            return generateDiscoverEventTarget(event, organization, location);
    }
}
exports.generateSingleErrorTarget = generateSingleErrorTarget;
function generateSingleTransactionTarget(event, organization, location, destination) {
    switch (destination) {
        case 'performance':
            return generatePerformanceEventTarget(event, organization, location);
        case 'discover':
        default:
            return generateDiscoverEventTarget(event, organization, location);
    }
}
exports.generateSingleTransactionTarget = generateSingleTransactionTarget;
function generateMultiTransactionsTarget(currentEvent, events, organization, groupType) {
    var queryResults = new tokenizeSearch_1.QueryResults([]);
    var eventIds = events.map(function (child) { return child.event_id; });
    for (var i = 0; i < eventIds.length; i++) {
        queryResults.addOp(i === 0 ? '(' : 'OR');
        queryResults.addQuery("id:" + eventIds[i]);
        if (i === eventIds.length - 1) {
            queryResults.addOp(')');
        }
    }
    var _a = utils_2.getTraceTimeRangeFromEvent(currentEvent), start = _a.start, end = _a.end;
    var traceEventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        name: groupType + " Transactions of Event ID " + currentEvent.id,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: queryResults.formatString(),
        projects: tslib_1.__spreadArray([], tslib_1.__read(new Set(events.map(function (child) { return child.project_id; })))),
        version: 2,
        start: start,
        end: end,
    });
    return traceEventView.getResultsViewUrlTarget(organization.slug);
}
exports.generateMultiTransactionsTarget = generateMultiTransactionsTarget;
function generateTraceTarget(event, organization) {
    var _a, _b, _c;
    var traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
    var dateSelection = getParams_1.getParams(utils_2.getTraceTimeRangeFromEvent(event));
    if (organization.features.includes('performance-view')) {
        // TODO(txiao): Should this persist the current query when going to trace view?
        return utils_3.getTraceDetailsUrl(organization, traceId, dateSelection, {});
    }
    var eventView = eventView_1.default.fromSavedQuery(tslib_1.__assign({ id: undefined, name: "Events with Trace ID " + traceId, fields: ['title', 'event.type', 'project', 'trace.span', 'timestamp'], orderby: '-timestamp', query: "trace:" + traceId, projects: organization.features.includes('global-views')
            ? [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
            : [Number(event.projectID)], version: 2 }, dateSelection));
    return eventView.getResultsViewUrlTarget(organization.slug);
}
exports.generateTraceTarget = generateTraceTarget;
//# sourceMappingURL=utils.jsx.map