Object.defineProperty(exports, "__esModule", { value: true });
exports.scrollToSpan = exports.getMeasurementBounds = exports.getMeasurements = exports.durationlessBrowserOps = exports.isEventFromBrowserJavaScriptSDK = exports.unwrapTreeDepth = exports.isOrphanTreeDepth = exports.parseTrace = exports.getTraceContext = exports.getSpanParentSpanID = exports.getSpanTraceID = exports.getSpanOperation = exports.getSpanID = exports.isOrphanSpan = exports.isGapSpan = exports.getTraceDateTimeRange = exports.generateRootSpan = exports.boundsGenerator = exports.parseSpanTimestamps = exports.TimestampStatus = exports.isValidSpanID = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var isNumber_1 = tslib_1.__importDefault(require("lodash/isNumber"));
var isString_1 = tslib_1.__importDefault(require("lodash/isString"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var event_1 = require("app/types/event");
var utils_1 = require("app/types/utils");
var constants_1 = require("app/utils/performance/vitals/constants");
var isValidSpanID = function (maybeSpanID) {
    return isString_1.default(maybeSpanID) && maybeSpanID.length > 0;
};
exports.isValidSpanID = isValidSpanID;
var normalizeTimestamps = function (spanBounds) {
    var startTimestamp = spanBounds.startTimestamp, endTimestamp = spanBounds.endTimestamp;
    if (startTimestamp > endTimestamp) {
        return { startTimestamp: endTimestamp, endTimestamp: startTimestamp };
    }
    return spanBounds;
};
var TimestampStatus;
(function (TimestampStatus) {
    TimestampStatus[TimestampStatus["Stable"] = 0] = "Stable";
    TimestampStatus[TimestampStatus["Reversed"] = 1] = "Reversed";
    TimestampStatus[TimestampStatus["Equal"] = 2] = "Equal";
})(TimestampStatus = exports.TimestampStatus || (exports.TimestampStatus = {}));
var parseSpanTimestamps = function (spanBounds) {
    var startTimestamp = spanBounds.startTimestamp;
    var endTimestamp = spanBounds.endTimestamp;
    if (startTimestamp < endTimestamp) {
        return TimestampStatus.Stable;
    }
    if (startTimestamp === endTimestamp) {
        return TimestampStatus.Equal;
    }
    return TimestampStatus.Reversed;
};
exports.parseSpanTimestamps = parseSpanTimestamps;
// given the start and end trace timestamps, and the view window, we want to generate a function
// that'll output the relative %'s for the width and placements relative to the left-hand side.
//
// The view window (viewStart and viewEnd) are percentage values (between 0% and 100%), they correspond to the window placement
// between the start and end trace timestamps.
var boundsGenerator = function (bounds) {
    var viewStart = bounds.viewStart, viewEnd = bounds.viewEnd;
    var _a = normalizeTimestamps({
        startTimestamp: bounds.traceStartTimestamp,
        endTimestamp: bounds.traceEndTimestamp,
    }), traceStartTimestamp = _a.startTimestamp, traceEndTimestamp = _a.endTimestamp;
    // viewStart and viewEnd are percentage values (%) of the view window relative to the left
    // side of the trace view minimap
    // invariant: viewStart <= viewEnd
    // duration of the entire trace in seconds
    var traceDuration = traceEndTimestamp - traceStartTimestamp;
    var viewStartTimestamp = traceStartTimestamp + viewStart * traceDuration;
    var viewEndTimestamp = traceEndTimestamp - (1 - viewEnd) * traceDuration;
    var viewDuration = viewEndTimestamp - viewStartTimestamp;
    return function (spanBounds) {
        // TODO: alberto.... refactor so this is impossible 😠
        if (traceDuration <= 0) {
            return {
                type: 'TRACE_TIMESTAMPS_EQUAL',
                isSpanVisibleInView: true,
            };
        }
        if (viewDuration <= 0) {
            return {
                type: 'INVALID_VIEW_WINDOW',
                isSpanVisibleInView: true,
            };
        }
        var _a = normalizeTimestamps(spanBounds), startTimestamp = _a.startTimestamp, endTimestamp = _a.endTimestamp;
        var timestampStatus = exports.parseSpanTimestamps(spanBounds);
        var start = (startTimestamp - viewStartTimestamp) / viewDuration;
        var end = (endTimestamp - viewStartTimestamp) / viewDuration;
        var isSpanVisibleInView = end > 0 && start < 1;
        switch (timestampStatus) {
            case TimestampStatus.Equal: {
                return {
                    type: 'TIMESTAMPS_EQUAL',
                    start: start,
                    width: 1,
                    // a span bar is visible even if they're at the extreme ends of the view selection.
                    // these edge cases are:
                    // start == end == 0, and
                    // start == end == 1
                    isSpanVisibleInView: end >= 0 && start <= 1,
                };
            }
            case TimestampStatus.Reversed: {
                return {
                    type: 'TIMESTAMPS_REVERSED',
                    start: start,
                    end: end,
                    isSpanVisibleInView: isSpanVisibleInView,
                };
            }
            case TimestampStatus.Stable: {
                return {
                    type: 'TIMESTAMPS_STABLE',
                    start: start,
                    end: end,
                    isSpanVisibleInView: isSpanVisibleInView,
                };
            }
            default: {
                var _exhaustiveCheck = timestampStatus;
                return _exhaustiveCheck;
            }
        }
    };
};
exports.boundsGenerator = boundsGenerator;
function generateRootSpan(trace) {
    var rootSpan = {
        trace_id: trace.traceID,
        span_id: trace.rootSpanID,
        parent_span_id: trace.parentSpanID,
        start_timestamp: trace.traceStartTimestamp,
        timestamp: trace.traceEndTimestamp,
        op: trace.op,
        description: trace.description,
        data: {},
        status: trace.rootSpanStatus,
    };
    return rootSpan;
}
exports.generateRootSpan = generateRootSpan;
// start and end are assumed to be unix timestamps with fractional seconds
function getTraceDateTimeRange(input) {
    var start = moment_1.default
        .unix(input.start)
        .subtract(12, 'hours')
        .utc()
        .format('YYYY-MM-DDTHH:mm:ss.SSS');
    var end = moment_1.default
        .unix(input.end)
        .add(12, 'hours')
        .utc()
        .format('YYYY-MM-DDTHH:mm:ss.SSS');
    return {
        start: start,
        end: end,
    };
}
exports.getTraceDateTimeRange = getTraceDateTimeRange;
function isGapSpan(span) {
    if ('type' in span) {
        return span.type === 'gap';
    }
    return false;
}
exports.isGapSpan = isGapSpan;
function isOrphanSpan(span) {
    if ('type' in span) {
        if (span.type === 'orphan') {
            return true;
        }
        if (span.type === 'gap') {
            return span.isOrphan;
        }
    }
    return false;
}
exports.isOrphanSpan = isOrphanSpan;
function getSpanID(span, defaultSpanID) {
    if (defaultSpanID === void 0) { defaultSpanID = ''; }
    if (isGapSpan(span)) {
        return defaultSpanID;
    }
    return span.span_id;
}
exports.getSpanID = getSpanID;
function getSpanOperation(span) {
    if (isGapSpan(span)) {
        return undefined;
    }
    return span.op;
}
exports.getSpanOperation = getSpanOperation;
function getSpanTraceID(span) {
    if (isGapSpan(span)) {
        return 'gap-span';
    }
    return span.trace_id;
}
exports.getSpanTraceID = getSpanTraceID;
function getSpanParentSpanID(span) {
    if (isGapSpan(span)) {
        return 'gap-span';
    }
    return span.parent_span_id;
}
exports.getSpanParentSpanID = getSpanParentSpanID;
function getTraceContext(event) {
    var _a;
    return (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
}
exports.getTraceContext = getTraceContext;
function parseTrace(event) {
    var _a;
    var spanEntry = event.entries.find(function (entry) {
        return entry.type === event_1.EntryType.SPANS;
    });
    var spans = (_a = spanEntry === null || spanEntry === void 0 ? void 0 : spanEntry.data) !== null && _a !== void 0 ? _a : [];
    var traceContext = getTraceContext(event);
    var traceID = (traceContext && traceContext.trace_id) || '';
    var rootSpanID = (traceContext && traceContext.span_id) || '';
    var rootSpanOpName = (traceContext && traceContext.op) || 'transaction';
    var description = traceContext && traceContext.description;
    var parentSpanID = traceContext && traceContext.parent_span_id;
    var rootSpanStatus = traceContext && traceContext.status;
    if (!spanEntry || spans.length <= 0) {
        return {
            op: rootSpanOpName,
            childSpans: {},
            traceStartTimestamp: event.startTimestamp,
            traceEndTimestamp: event.endTimestamp,
            traceID: traceID,
            rootSpanID: rootSpanID,
            rootSpanStatus: rootSpanStatus,
            parentSpanID: parentSpanID,
            numOfSpans: 0,
            spans: [],
            description: description,
        };
    }
    // any span may be a parent of another span
    var potentialParents = new Set(spans.map(function (span) {
        return span.span_id;
    }));
    // the root transaction span is a parent of all other spans
    potentialParents.add(rootSpanID);
    // we reduce spans to become an object mapping span ids to their children
    var init = {
        op: rootSpanOpName,
        childSpans: {},
        traceStartTimestamp: event.startTimestamp,
        traceEndTimestamp: event.endTimestamp,
        traceID: traceID,
        rootSpanID: rootSpanID,
        rootSpanStatus: rootSpanStatus,
        parentSpanID: parentSpanID,
        numOfSpans: spans.length,
        spans: spans,
        description: description,
    };
    var reduced = spans.reduce(function (acc, inputSpan) {
        var _a;
        var span = inputSpan;
        var parentSpanId = getSpanParentSpanID(span);
        var hasParent = parentSpanId && potentialParents.has(parentSpanId);
        if (!exports.isValidSpanID(parentSpanId) || !hasParent) {
            // this span is considered an orphan with respect to the spans within this transaction.
            // although the span is an orphan, it's still a descendant of this transaction,
            // so we set its parent span id to be the root transaction span's id
            span.parent_span_id = rootSpanID;
            span = tslib_1.__assign({ type: 'orphan' }, span);
        }
        utils_1.assert(span.parent_span_id);
        // get any span children whose parent_span_id is equal to span.parent_span_id,
        // otherwise start with an empty array
        var spanChildren = (_a = acc.childSpans[span.parent_span_id]) !== null && _a !== void 0 ? _a : [];
        spanChildren.push(span);
        set_1.default(acc.childSpans, span.parent_span_id, spanChildren);
        // set trace start & end timestamps based on given span's start and end timestamps
        if (!acc.traceStartTimestamp || span.start_timestamp < acc.traceStartTimestamp) {
            acc.traceStartTimestamp = span.start_timestamp;
        }
        // establish trace end timestamp
        var hasEndTimestamp = isNumber_1.default(span.timestamp);
        if (!acc.traceEndTimestamp) {
            if (hasEndTimestamp) {
                acc.traceEndTimestamp = span.timestamp;
                return acc;
            }
            acc.traceEndTimestamp = span.start_timestamp;
            return acc;
        }
        if (hasEndTimestamp && span.timestamp > acc.traceEndTimestamp) {
            acc.traceEndTimestamp = span.timestamp;
            return acc;
        }
        if (span.start_timestamp > acc.traceEndTimestamp) {
            acc.traceEndTimestamp = span.start_timestamp;
        }
        return acc;
    }, init);
    // sort span children
    Object.values(reduced.childSpans).forEach(function (spanChildren) {
        spanChildren.sort(sortSpans);
    });
    return reduced;
}
exports.parseTrace = parseTrace;
function sortSpans(firstSpan, secondSpan) {
    // orphan spans come after non-orphan spans.
    if (isOrphanSpan(firstSpan) && !isOrphanSpan(secondSpan)) {
        // sort secondSpan before firstSpan
        return 1;
    }
    if (!isOrphanSpan(firstSpan) && isOrphanSpan(secondSpan)) {
        // sort firstSpan before secondSpan
        return -1;
    }
    // sort spans by their start timestamp in ascending order
    if (firstSpan.start_timestamp < secondSpan.start_timestamp) {
        // sort firstSpan before secondSpan
        return -1;
    }
    if (firstSpan.start_timestamp === secondSpan.start_timestamp) {
        return 0;
    }
    // sort secondSpan before firstSpan
    return 1;
}
function isOrphanTreeDepth(treeDepth) {
    if (typeof treeDepth === 'number') {
        return false;
    }
    return (treeDepth === null || treeDepth === void 0 ? void 0 : treeDepth.type) === 'orphan';
}
exports.isOrphanTreeDepth = isOrphanTreeDepth;
function unwrapTreeDepth(treeDepth) {
    if (isOrphanTreeDepth(treeDepth)) {
        return treeDepth.depth;
    }
    return treeDepth;
}
exports.unwrapTreeDepth = unwrapTreeDepth;
function isEventFromBrowserJavaScriptSDK(event) {
    var _a;
    var sdkName = (_a = event.sdk) === null || _a === void 0 ? void 0 : _a.name;
    if (!sdkName) {
        return false;
    }
    // based on https://github.com/getsentry/sentry-javascript/blob/master/packages/browser/src/version.ts
    return [
        'sentry.javascript.browser',
        'sentry.javascript.react',
        'sentry.javascript.gatsby',
        'sentry.javascript.ember',
        'sentry.javascript.vue',
        'sentry.javascript.angular',
        'sentry.javascript.nextjs',
    ].includes(sdkName.toLowerCase());
}
exports.isEventFromBrowserJavaScriptSDK = isEventFromBrowserJavaScriptSDK;
// Durationless ops from: https://github.com/getsentry/sentry-javascript/blob/0defcdcc2dfe719343efc359d58c3f90743da2cd/packages/apm/src/integrations/tracing.ts#L629-L688
// PerformanceMark: Duration is 0 as per https://developer.mozilla.org/en-US/docs/Web/API/PerformanceMark
// PerformancePaintTiming: Duration is 0 as per https://developer.mozilla.org/en-US/docs/Web/API/PerformancePaintTiming
exports.durationlessBrowserOps = ['mark', 'paint'];
function hasFailedThreshold(marks) {
    var names = Object.keys(marks);
    var records = Object.values(constants_1.WEB_VITAL_DETAILS).filter(function (vital) {
        return names.includes(vital.slug);
    });
    return records.some(function (record) {
        var value = marks[record.slug];
        if (typeof value === 'number' && typeof record.poorThreshold === 'number') {
            return value >= record.poorThreshold;
        }
        return false;
    });
}
function getMeasurements(event) {
    if (!event.measurements) {
        return new Map();
    }
    var measurements = Object.keys(event.measurements)
        .filter(function (name) { return name.startsWith('mark.'); })
        .map(function (name) {
        var slug = name.slice('mark.'.length);
        var associatedMeasurement = event.measurements[slug];
        return {
            name: name,
            timestamp: event.measurements[name].value,
            value: associatedMeasurement ? associatedMeasurement.value : undefined,
        };
    });
    var mergedMeasurements = new Map();
    measurements.forEach(function (measurement) {
        var _a, _b;
        var name = measurement.name.slice('mark.'.length);
        var value = measurement.value;
        if (mergedMeasurements.has(measurement.timestamp)) {
            var verticalMark = mergedMeasurements.get(measurement.timestamp);
            verticalMark.marks = tslib_1.__assign(tslib_1.__assign({}, verticalMark.marks), (_a = {}, _a[name] = value, _a));
            if (!verticalMark.failedThreshold) {
                verticalMark.failedThreshold = hasFailedThreshold(verticalMark.marks);
            }
            mergedMeasurements.set(measurement.timestamp, verticalMark);
            return;
        }
        var marks = (_b = {},
            _b[name] = value,
            _b);
        mergedMeasurements.set(measurement.timestamp, {
            marks: marks,
            failedThreshold: hasFailedThreshold(marks),
        });
    });
    return mergedMeasurements;
}
exports.getMeasurements = getMeasurements;
function getMeasurementBounds(timestamp, generateBounds) {
    var bounds = generateBounds({
        startTimestamp: timestamp,
        endTimestamp: timestamp,
    });
    switch (bounds.type) {
        case 'TRACE_TIMESTAMPS_EQUAL':
        case 'INVALID_VIEW_WINDOW': {
            return {
                warning: undefined,
                left: undefined,
                width: undefined,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        case 'TIMESTAMPS_EQUAL': {
            return {
                warning: undefined,
                left: bounds.start,
                width: 0.00001,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        case 'TIMESTAMPS_REVERSED': {
            return {
                warning: undefined,
                left: bounds.start,
                width: bounds.end - bounds.start,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        case 'TIMESTAMPS_STABLE': {
            return {
                warning: void 0,
                left: bounds.start,
                width: bounds.end - bounds.start,
                isSpanVisibleInView: bounds.isSpanVisibleInView,
            };
        }
        default: {
            var _exhaustiveCheck = bounds;
            return _exhaustiveCheck;
        }
    }
}
exports.getMeasurementBounds = getMeasurementBounds;
function scrollToSpan(spanId, scrollToHash, location) {
    return function (e) {
        // do not use the default anchor behaviour
        // because it will be hidden behind the minimap
        e.preventDefault();
        var hash = "#span-" + spanId;
        scrollToHash(hash);
        // TODO(txiao): This is causing a rerender of the whole page,
        // which can be slow.
        //
        // make sure to update the location
        react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, location), { hash: hash }));
    };
}
exports.scrollToSpan = scrollToSpan;
//# sourceMappingURL=utils.jsx.map