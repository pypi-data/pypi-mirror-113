Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isFinite_1 = tslib_1.__importDefault(require("lodash/isFinite"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/events/interfaces/spans/utils");
var utils_2 = require("app/components/performance/waterfall/utils");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var event_1 = require("app/types/event");
var OtherOperation = Symbol('Other');
var TOP_N_SPANS = 4;
var OpsBreakdown = /** @class */ (function (_super) {
    tslib_1.__extends(OpsBreakdown, _super);
    function OpsBreakdown() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OpsBreakdown.prototype.getTransactionEvent = function () {
        var event = this.props.event;
        if (event.type === 'transaction') {
            return event;
        }
        return undefined;
    };
    OpsBreakdown.prototype.generateStats = function () {
        var _a, _b;
        var _c = this.props, topN = _c.topN, operationNameFilters = _c.operationNameFilters;
        var event = this.getTransactionEvent();
        if (!event) {
            return [];
        }
        var traceContext = (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
        if (!traceContext) {
            return [];
        }
        var spanEntry = event.entries.find(function (entry) {
            return entry.type === event_1.EntryType.SPANS;
        });
        var spans = (_b = spanEntry === null || spanEntry === void 0 ? void 0 : spanEntry.data) !== null && _b !== void 0 ? _b : [];
        var rootSpan = {
            op: traceContext.op,
            timestamp: event.endTimestamp,
            start_timestamp: event.startTimestamp,
            trace_id: traceContext.trace_id || '',
            span_id: traceContext.span_id || '',
            data: {},
        };
        spans =
            spans.length > 0
                ? spans
                : // if there are no descendent spans, then use the transaction root span
                    [rootSpan];
        // Filter spans by operation name
        if (operationNameFilters.type === 'active_filter') {
            spans = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(spans)), [rootSpan]);
            spans = spans.filter(function (span) {
                var operationName = utils_1.getSpanOperation(span);
                var shouldFilterOut = typeof operationName === 'string' &&
                    !operationNameFilters.operationNames.has(operationName);
                return !shouldFilterOut;
            });
        }
        var operationNameIntervals = spans.reduce(function (intervals, span) {
            var startTimestamp = span.start_timestamp;
            var endTimestamp = span.timestamp;
            if (endTimestamp < startTimestamp) {
                // reverse timestamps
                startTimestamp = span.timestamp;
                endTimestamp = span.start_timestamp;
            }
            // invariant: startTimestamp <= endTimestamp
            var operationName = span.op;
            if (typeof operationName !== 'string') {
                // a span with no operation name is considered an 'unknown' op
                operationName = 'unknown';
            }
            var cover = [startTimestamp, endTimestamp];
            var operationNameInterval = intervals[operationName];
            if (!Array.isArray(operationNameInterval)) {
                intervals[operationName] = [cover];
                return intervals;
            }
            operationNameInterval.push(cover);
            intervals[operationName] = mergeInterval(operationNameInterval);
            return intervals;
        }, {});
        var operationNameCoverage = Object.entries(operationNameIntervals).reduce(function (acc, _a) {
            var _b = tslib_1.__read(_a, 2), operationName = _b[0], intervals = _b[1];
            var duration = intervals.reduce(function (sum, _a) {
                var _b = tslib_1.__read(_a, 2), start = _b[0], end = _b[1];
                return sum + Math.abs(end - start);
            }, 0);
            acc[operationName] = duration;
            return acc;
        }, {});
        var sortedOpsBreakdown = Object.entries(operationNameCoverage).sort(function (first, second) {
            var firstDuration = first[1];
            var secondDuration = second[1];
            if (firstDuration === secondDuration) {
                return 0;
            }
            if (firstDuration < secondDuration) {
                // sort second before first
                return 1;
            }
            // otherwise, sort first before second
            return -1;
        });
        var breakdown = sortedOpsBreakdown
            .slice(0, topN)
            .map(function (_a) {
            var _b = tslib_1.__read(_a, 2), operationName = _b[0], duration = _b[1];
            return {
                name: operationName,
                // percentage to be recalculated after the ops breakdown group is decided
                percentage: 0,
                totalInterval: duration,
            };
        });
        var other = sortedOpsBreakdown.slice(topN).reduce(function (accOther, _a) {
            var _b = tslib_1.__read(_a, 2), _operationName = _b[0], duration = _b[1];
            accOther.totalInterval += duration;
            return accOther;
        }, {
            name: OtherOperation,
            // percentage to be recalculated after the ops breakdown group is decided
            percentage: 0,
            totalInterval: 0,
        });
        if (other.totalInterval > 0) {
            breakdown.push(other);
        }
        // calculate breakdown total duration
        var total = breakdown.reduce(function (sum, operationNameGroup) {
            return sum + operationNameGroup.totalInterval;
        }, 0);
        // recalculate percentage values
        breakdown.forEach(function (operationNameGroup) {
            operationNameGroup.percentage = operationNameGroup.totalInterval / total;
        });
        return breakdown;
    };
    OpsBreakdown.prototype.render = function () {
        var hideHeader = this.props.hideHeader;
        var event = this.getTransactionEvent();
        if (!event) {
            return null;
        }
        var breakdown = this.generateStats();
        var contents = breakdown.map(function (currOp) {
            var name = currOp.name, percentage = currOp.percentage, totalInterval = currOp.totalInterval;
            var isOther = name === OtherOperation;
            var operationName = typeof name === 'string' ? name : locale_1.t('Other');
            var durLabel = Math.round(totalInterval * 1000 * 100) / 100;
            var pctLabel = isFinite_1.default(percentage) ? Math.round(percentage * 100) : '∞';
            var opsColor = utils_2.pickBarColour(operationName);
            return (<OpsLine key={operationName}>
          <OpsNameContainer>
            <OpsDot style={{ backgroundColor: isOther ? 'transparent' : opsColor }}/>
            <OpsName>{operationName}</OpsName>
          </OpsNameContainer>
          <OpsContent>
            <Dur>{durLabel}ms</Dur>
            <Pct>{pctLabel}%</Pct>
          </OpsContent>
        </OpsLine>);
        });
        if (!hideHeader) {
            return (<StyledBreakdown>
          <styles_1.SectionHeading>
            {locale_1.t('Operation Breakdown')}
            <questionTooltip_1.default position="top" size="sm" containerDisplayMode="block" title={locale_1.t('Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once. Percentages are calculated by dividing the summed span durations by the total of all span durations.')}/>
          </styles_1.SectionHeading>
          {contents}
        </StyledBreakdown>);
        }
        return <StyledBreakdownNoHeader>{contents}</StyledBreakdownNoHeader>;
    };
    OpsBreakdown.defaultProps = {
        topN: TOP_N_SPANS,
        hideHeader: false,
    };
    return OpsBreakdown;
}(react_1.Component));
var StyledBreakdown = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(4));
var StyledBreakdownNoHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " ", ";\n"], ["\n  font-size: ", ";\n  margin: ", " ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(2), space_1.default(3));
var OpsLine = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  * + * {\n    margin-left: ", ";\n  }\n"])), space_1.default(0.5), space_1.default(0.5));
var OpsDot = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n"], ["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n"])), space_1.default(1));
var OpsContent = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var OpsNameContainer = styled_1.default(OpsContent)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var OpsName = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])));
var Dur = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Pct = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  min-width: 40px;\n  text-align: right;\n"], ["\n  min-width: 40px;\n  text-align: right;\n"])));
function mergeInterval(intervals) {
    var e_1, _a;
    // sort intervals by start timestamps
    intervals.sort(function (first, second) {
        if (first[0] < second[0]) {
            // sort first before second
            return -1;
        }
        if (second[0] < first[0]) {
            // sort second before first
            return 1;
        }
        return 0;
    });
    // array of disjoint intervals
    var merged = [];
    try {
        for (var intervals_1 = tslib_1.__values(intervals), intervals_1_1 = intervals_1.next(); !intervals_1_1.done; intervals_1_1 = intervals_1.next()) {
            var currentInterval = intervals_1_1.value;
            if (merged.length === 0) {
                merged.push(currentInterval);
                continue;
            }
            var lastInterval = merged[merged.length - 1];
            var lastIntervalEnd = lastInterval[1];
            var _b = tslib_1.__read(currentInterval, 2), currentIntervalStart = _b[0], currentIntervalEnd = _b[1];
            if (lastIntervalEnd < currentIntervalStart) {
                // if currentInterval does not overlap with lastInterval,
                // then add currentInterval
                merged.push(currentInterval);
                continue;
            }
            // currentInterval and lastInterval overlaps; so we merge these intervals
            // invariant: lastIntervalStart <= currentIntervalStart
            lastInterval[1] = Math.max(lastIntervalEnd, currentIntervalEnd);
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (intervals_1_1 && !intervals_1_1.done && (_a = intervals_1.return)) _a.call(intervals_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return merged;
}
exports.default = OpsBreakdown;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=opsBreakdown.jsx.map