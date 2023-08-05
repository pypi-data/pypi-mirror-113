var _a, _b, _c, _d;
Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledIconArrow = exports.transformEventStatsSmoothed = exports.replaceSmoothedSeriesName = exports.replaceSeriesName = exports.smoothTrend = exports.movingAverage = exports.getUnselectedSeries = exports.getSelectedQueryKey = exports.normalizeTrends = exports.transformValueDelta = exports.modifyTrendsViewDefaultPeriod = exports.modifyTrendView = exports.getTrendProjectId = exports.transformDeltaSpread = exports.generateTrendFunctionAsString = exports.getCurrentTrendParameter = exports.getCurrentTrendFunction = exports.resetCursors = exports.trendCursorNames = exports.trendUnselectedSeries = exports.trendSelectedQueryKeys = exports.trendToColor = exports.getTrendsParameters = exports.TRENDS_FUNCTIONS = exports.DEFAULT_MAX_DURATION = exports.DEFAULT_TRENDS_STATS_PERIOD = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var ASAP_1 = require("downsample/methods/ASAP");
var moment_1 = tslib_1.__importDefault(require("moment"));
var utils_1 = require("app/components/charts/utils");
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var types_1 = require("./types");
exports.DEFAULT_TRENDS_STATS_PERIOD = '14d';
exports.DEFAULT_MAX_DURATION = '15min';
exports.TRENDS_FUNCTIONS = [
    {
        label: 'p50',
        field: types_1.TrendFunctionField.P50,
        alias: 'percentile_range',
        legendLabel: 'p50',
    },
    {
        label: 'p75',
        field: types_1.TrendFunctionField.P75,
        alias: 'percentile_range',
        legendLabel: 'p75',
    },
    {
        label: 'p95',
        field: types_1.TrendFunctionField.P95,
        alias: 'percentile_range',
        legendLabel: 'p95',
    },
    {
        label: 'p99',
        field: types_1.TrendFunctionField.P99,
        alias: 'percentile_range',
        legendLabel: 'p99',
    },
    {
        label: 'average',
        field: types_1.TrendFunctionField.AVG,
        alias: 'avg_range',
        legendLabel: 'average',
    },
];
var TRENDS_PARAMETERS = [
    {
        label: 'Duration',
        column: types_1.TrendColumnField.DURATION,
    },
    {
        label: 'LCP',
        column: types_1.TrendColumnField.LCP,
    },
    {
        label: 'FCP',
        column: types_1.TrendColumnField.FCP,
    },
    {
        label: 'FID',
        column: types_1.TrendColumnField.FID,
    },
    {
        label: 'CLS',
        column: types_1.TrendColumnField.CLS,
    },
];
// TODO(perf): Merge with above after ops breakdown feature is mainlined.
var SPANS_TRENDS_PARAMETERS = [
    {
        label: 'Spans (http)',
        column: types_1.TrendColumnField.SPANS_HTTP,
    },
    {
        label: 'Spans (db)',
        column: types_1.TrendColumnField.SPANS_DB,
    },
    {
        label: 'Spans (browser)',
        column: types_1.TrendColumnField.SPANS_BROWSER,
    },
    {
        label: 'Spans (resource)',
        column: types_1.TrendColumnField.SPANS_RESOURCE,
    },
];
function getTrendsParameters(_a) {
    var _b = _a === void 0 ? { canSeeSpanOpTrends: false } : _a, canSeeSpanOpTrends = _b.canSeeSpanOpTrends;
    return canSeeSpanOpTrends
        ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(TRENDS_PARAMETERS)), tslib_1.__read(SPANS_TRENDS_PARAMETERS)) : tslib_1.__spreadArray([], tslib_1.__read(TRENDS_PARAMETERS));
}
exports.getTrendsParameters = getTrendsParameters;
exports.trendToColor = (_a = {},
    _a[types_1.TrendChangeType.IMPROVED] = {
        lighter: theme_1.default.green200,
        default: theme_1.default.green300,
    },
    _a[types_1.TrendChangeType.REGRESSION] = {
        lighter: theme_1.default.red200,
        default: theme_1.default.red300,
    },
    _a);
exports.trendSelectedQueryKeys = (_b = {},
    _b[types_1.TrendChangeType.IMPROVED] = 'improvedSelected',
    _b[types_1.TrendChangeType.REGRESSION] = 'regressionSelected',
    _b);
exports.trendUnselectedSeries = (_c = {},
    _c[types_1.TrendChangeType.IMPROVED] = 'improvedUnselectedSeries',
    _c[types_1.TrendChangeType.REGRESSION] = 'regressionUnselectedSeries',
    _c);
exports.trendCursorNames = (_d = {},
    _d[types_1.TrendChangeType.IMPROVED] = 'improvedCursor',
    _d[types_1.TrendChangeType.REGRESSION] = 'regressionCursor',
    _d);
function resetCursors() {
    var cursors = {};
    Object.values(exports.trendCursorNames).forEach(function (cursor) { return (cursors[cursor] = undefined); }); // Resets both cursors
    return cursors;
}
exports.resetCursors = resetCursors;
function getCurrentTrendFunction(location) {
    var _a;
    var trendFunctionField = queryString_1.decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.trendFunction);
    var trendFunction = exports.TRENDS_FUNCTIONS.find(function (_a) {
        var field = _a.field;
        return field === trendFunctionField;
    });
    return trendFunction || exports.TRENDS_FUNCTIONS[0];
}
exports.getCurrentTrendFunction = getCurrentTrendFunction;
function getCurrentTrendParameter(location) {
    var _a;
    var trendParameterLabel = queryString_1.decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.trendParameter);
    var trendParameter = TRENDS_PARAMETERS.find(function (_a) {
        var label = _a.label;
        return label === trendParameterLabel;
    });
    return trendParameter || TRENDS_PARAMETERS[0];
}
exports.getCurrentTrendParameter = getCurrentTrendParameter;
function generateTrendFunctionAsString(trendFunction, trendParameter) {
    return fields_1.generateFieldAsString({
        kind: 'function',
        function: [trendFunction, trendParameter, undefined, undefined],
    });
}
exports.generateTrendFunctionAsString = generateTrendFunctionAsString;
function transformDeltaSpread(from, to) {
    var fromSeconds = from / 1000;
    var toSeconds = to / 1000;
    var showDigits = from > 1000 || to > 1000 || from < 10 || to < 10; // Show digits consistently if either has them
    return (<span>
      <duration_1.default seconds={fromSeconds} fixedDigits={showDigits ? 1 : 0} abbreviation/>
      <exports.StyledIconArrow direction="right" size="xs"/>
      <duration_1.default seconds={toSeconds} fixedDigits={showDigits ? 1 : 0} abbreviation/>
    </span>);
}
exports.transformDeltaSpread = transformDeltaSpread;
function getTrendProjectId(trend, projects) {
    if (!trend.project || !projects) {
        return undefined;
    }
    var transactionProject = projects.find(function (project) { return project.slug === trend.project; });
    return transactionProject === null || transactionProject === void 0 ? void 0 : transactionProject.id;
}
exports.getTrendProjectId = getTrendProjectId;
function modifyTrendView(trendView, location, trendsType, isProjectOnly) {
    var trendFunction = getCurrentTrendFunction(location);
    var trendParameter = getCurrentTrendParameter(location);
    var transactionField = isProjectOnly ? [] : ['transaction'];
    var fields = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(transactionField)), ['project']).map(function (field) { return ({
        field: field,
    }); });
    var trendSort = {
        field: 'trend_percentage()',
        kind: 'asc',
    };
    trendView.trendType = trendsType;
    if (trendsType === types_1.TrendChangeType.REGRESSION) {
        trendSort.kind = 'desc';
    }
    if (trendFunction && trendParameter) {
        trendView.trendFunction = generateTrendFunctionAsString(trendFunction.field, trendParameter.column);
    }
    trendView.query = getLimitTransactionItems(trendView.query);
    trendView.interval = getQueryInterval(location, trendView);
    trendView.sorts = [trendSort];
    trendView.fields = fields;
}
exports.modifyTrendView = modifyTrendView;
function modifyTrendsViewDefaultPeriod(eventView, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    if (!query.statsPeriod && !hasStartAndEnd) {
        eventView.statsPeriod = exports.DEFAULT_TRENDS_STATS_PERIOD;
    }
    return eventView;
}
exports.modifyTrendsViewDefaultPeriod = modifyTrendsViewDefaultPeriod;
function getQueryInterval(location, eventView) {
    var _a;
    var intervalFromQueryParam = queryString_1.decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.interval);
    var start = eventView.start, end = eventView.end, statsPeriod = eventView.statsPeriod;
    var datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    var intervalFromSmoothing = utils_1.getInterval(datetimeSelection, true);
    return intervalFromQueryParam || intervalFromSmoothing;
}
function transformValueDelta(value, trendType) {
    var absoluteValue = Math.abs(value);
    var changeLabel = trendType === types_1.TrendChangeType.REGRESSION ? locale_1.t('slower') : locale_1.t('faster');
    var seconds = absoluteValue / 1000;
    var fixedDigits = absoluteValue > 1000 || absoluteValue < 10 ? 1 : 0;
    return (<span>
      <duration_1.default seconds={seconds} fixedDigits={fixedDigits} abbreviation/> {changeLabel}
    </span>);
}
exports.transformValueDelta = transformValueDelta;
/**
 * This will normalize the trends transactions while the current trend function and current data are out of sync
 * To minimize extra renders with missing results.
 */
function normalizeTrends(data) {
    var received_at = moment_1.default(); // Adding the received time for the transaction so calls to get baseline always line up with the transaction
    return data.map(function (row) {
        return tslib_1.__assign(tslib_1.__assign({}, row), { received_at: received_at, transaction: row.transaction });
    });
}
exports.normalizeTrends = normalizeTrends;
function getSelectedQueryKey(trendChangeType) {
    return exports.trendSelectedQueryKeys[trendChangeType];
}
exports.getSelectedQueryKey = getSelectedQueryKey;
function getUnselectedSeries(trendChangeType) {
    return exports.trendUnselectedSeries[trendChangeType];
}
exports.getUnselectedSeries = getUnselectedSeries;
function movingAverage(data, index, size) {
    return (data
        .slice(index - size, index)
        .map(function (a) { return a.value; })
        .reduce(function (a, b) { return a + b; }, 0) / size);
}
exports.movingAverage = movingAverage;
/**
 * This function applies defaults for trend and count percentage, and adds the confidence limit to the query
 */
function getLimitTransactionItems(query) {
    var limitQuery = tokenizeSearch_1.tokenizeSearch(query);
    if (!limitQuery.hasTag('count_percentage()')) {
        limitQuery.addTagValues('count_percentage()', ['>0.25', '<4']);
    }
    if (!limitQuery.hasTag('trend_percentage()')) {
        limitQuery.addTagValues('trend_percentage()', ['>0%']);
    }
    if (!limitQuery.hasTag('confidence()')) {
        limitQuery.addTagValues('confidence()', ['>6']);
    }
    return limitQuery.formatString();
}
var smoothTrend = function (data, resolution) {
    if (resolution === void 0) { resolution = 100; }
    return ASAP_1.ASAP(data, resolution);
};
exports.smoothTrend = smoothTrend;
var replaceSeriesName = function (seriesName) {
    return ['p50', 'p75'].find(function (aggregate) { return seriesName.includes(aggregate); });
};
exports.replaceSeriesName = replaceSeriesName;
var replaceSmoothedSeriesName = function (seriesName) {
    return "Smoothed " + ['p50', 'p75'].find(function (aggregate) { return seriesName.includes(aggregate); });
};
exports.replaceSmoothedSeriesName = replaceSmoothedSeriesName;
function transformEventStatsSmoothed(data, seriesName) {
    var e_1, _a;
    var minValue = Number.MAX_SAFE_INTEGER;
    var maxValue = 0;
    if (!data) {
        return {
            maxValue: maxValue,
            minValue: minValue,
            smoothedResults: undefined,
        };
    }
    var smoothedResults = [];
    try {
        for (var data_1 = tslib_1.__values(data), data_1_1 = data_1.next(); !data_1_1.done; data_1_1 = data_1.next()) {
            var current = data_1_1.value;
            var currentData = current.data;
            var resultData = [];
            var smoothed = exports.smoothTrend(currentData.map(function (_a) {
                var name = _a.name, value = _a.value;
                return [Number(name), value];
            }));
            for (var i = 0; i < smoothed.length; i++) {
                var point = smoothed[i];
                var value = point.y;
                resultData.push({
                    name: point.x,
                    value: value,
                });
                if (!isNaN(value)) {
                    var rounded = Math.round(value);
                    minValue = Math.min(rounded, minValue);
                    maxValue = Math.max(rounded, maxValue);
                }
            }
            smoothedResults.push({
                seriesName: seriesName || current.seriesName || 'Current',
                data: resultData,
                lineStyle: current.lineStyle,
                color: current.color,
            });
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (data_1_1 && !data_1_1.done && (_a = data_1.return)) _a.call(data_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return {
        minValue: minValue,
        maxValue: maxValue,
        smoothedResults: smoothedResults,
    };
}
exports.transformEventStatsSmoothed = transformEventStatsSmoothed;
exports.StyledIconArrow = styled_1.default(icons_1.IconArrow)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n"], ["\n  margin: 0 ", ";\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=utils.jsx.map