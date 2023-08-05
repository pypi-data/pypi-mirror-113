Object.defineProperty(exports, "__esModule", { value: true });
exports.fillCrashFreeChartDataFromSessionsReponse = exports.fillChartDataFromSessionsResponse = exports.getTotalsFromSessionsResponse = exports.sortSessionSeries = exports.isOtherSeries = exports.initOtherSessionDurationChartData = exports.initSessionDurationChartData = exports.initOtherCrashFreeChartData = exports.initCrashFreeChartData = exports.initOtherSessionsBreakdownChartData = exports.initSessionsBreakdownChartData = exports.getReleaseEventView = exports.getInterval = void 0;
var tslib_1 = require("tslib");
var color_1 = tslib_1.__importDefault(require("color"));
var utils_1 = require("app/components/charts/utils");
var chartPalette_1 = tslib_1.__importDefault(require("app/constants/chartPalette"));
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var dates_1 = require("app/utils/dates");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var formatters_1 = require("app/utils/formatters");
var constants_1 = require("app/utils/performance/vitals/constants");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_3 = require("app/views/releases/utils");
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var releaseChartControls_1 = require("./releaseChartControls");
var SESSIONS_CHART_PALETTE = chartPalette_1.default[3];
function getInterval(datetimeObj, _a) {
    var _b = _a === void 0 ? {} : _a, highFidelity = _b.highFidelity;
    var diffInMinutes = utils_1.getDiffInMinutes(datetimeObj);
    if (highFidelity &&
        diffInMinutes < 360 // limit on backend is set to six hour
    ) {
        return '5m';
    }
    if (diffInMinutes > utils_1.TWO_WEEKS) {
        return '6h';
    }
    else {
        return '1h';
    }
}
exports.getInterval = getInterval;
function getReleaseEventView(selection, version, yAxis, eventType, vitalType, organization, 
/**
 * Indicates that we're only interested in the current release.
 * This is useful for the event meta end point where we don't want
 * to include the other releases.
 */
currentOnly) {
    if (eventType === void 0) { eventType = releaseChartControls_1.EventType.ALL; }
    if (vitalType === void 0) { vitalType = fields_1.WebVital.LCP; }
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period;
    var releaseFilter = currentOnly ? "release:" + version : '';
    var toOther = "to_other(release,\"" + utils_2.escapeDoubleQuotes(version) + "\",others,current)";
    // this orderby ensures that the order is [others, current]
    var toOtherAlias = fields_1.getAggregateAlias(toOther);
    var baseQuery = {
        id: undefined,
        version: 2,
        name: locale_1.t('Release') + " " + formatters_1.formatVersion(version),
        fields: ["count()", toOther],
        orderby: toOtherAlias,
        range: period,
        environment: environments,
        projects: projects,
        start: start ? dates_1.getUtcDateString(start) : undefined,
        end: end ? dates_1.getUtcDateString(end) : undefined,
    };
    switch (yAxis) {
        case releaseChartControls_1.YAxis.FAILED_TRANSACTIONS:
            var statusFilters = ['ok', 'cancelled', 'unknown'].map(function (s) { return "!transaction.status:" + s; });
            return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { query: new tokenizeSearch_1.QueryResults(tslib_1.__spreadArray(['event.type:transaction', releaseFilter], tslib_1.__read(statusFilters)).filter(Boolean)).formatString() }));
        case releaseChartControls_1.YAxis.COUNT_VITAL:
        case releaseChartControls_1.YAxis.COUNT_DURATION:
            var column = yAxis === releaseChartControls_1.YAxis.COUNT_DURATION ? 'transaction.duration' : vitalType;
            var threshold = yAxis === releaseChartControls_1.YAxis.COUNT_DURATION
                ? organization === null || organization === void 0 ? void 0 : organization.apdexThreshold
                : constants_1.WEB_VITAL_DETAILS[vitalType].poorThreshold;
            return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { query: new tokenizeSearch_1.QueryResults([
                    'event.type:transaction',
                    releaseFilter,
                    threshold ? column + ":>" + threshold : '',
                ].filter(Boolean)).formatString() }));
        case releaseChartControls_1.YAxis.EVENTS:
            var eventTypeFilter = eventType === releaseChartControls_1.EventType.ALL ? '' : "event.type:" + eventType;
            return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { query: new tokenizeSearch_1.QueryResults([releaseFilter, eventTypeFilter].filter(Boolean)).formatString() }));
        default:
            return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { fields: ['issue', 'title', 'count()', 'count_unique(user)', 'project'], query: new tokenizeSearch_1.QueryResults([
                    "release:" + version,
                    '!event.type:transaction',
                ]).formatString(), orderby: '-count' }));
    }
}
exports.getReleaseEventView = getReleaseEventView;
function initSessionsBreakdownChartData() {
    return {
        healthy: {
            seriesName: sessionTerm_1.sessionTerm.healthy,
            data: [],
            color: SESSIONS_CHART_PALETTE[3],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[3],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        errored: {
            seriesName: sessionTerm_1.sessionTerm.errored,
            data: [],
            color: SESSIONS_CHART_PALETTE[0],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[0],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        abnormal: {
            seriesName: sessionTerm_1.sessionTerm.abnormal,
            data: [],
            color: SESSIONS_CHART_PALETTE[1],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[1],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        crashed: {
            seriesName: sessionTerm_1.sessionTerm.crashed,
            data: [],
            color: SESSIONS_CHART_PALETTE[2],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[2],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initSessionsBreakdownChartData = initSessionsBreakdownChartData;
function initOtherSessionsBreakdownChartData() {
    return tslib_1.__assign({ healthy: {
            seriesName: sessionTerm_1.sessionTerm.otherHealthy,
            data: [],
            color: SESSIONS_CHART_PALETTE[3],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[3],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, errored: {
            seriesName: sessionTerm_1.sessionTerm.otherErrored,
            data: [],
            color: SESSIONS_CHART_PALETTE[0],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[0],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, abnormal: {
            seriesName: sessionTerm_1.sessionTerm.otherAbnormal,
            data: [],
            color: SESSIONS_CHART_PALETTE[1],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[1],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, crashed: {
            seriesName: sessionTerm_1.sessionTerm.otherCrashed,
            data: [],
            color: SESSIONS_CHART_PALETTE[2],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[2],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        } }, initOtherReleasesChartData());
}
exports.initOtherSessionsBreakdownChartData = initOtherSessionsBreakdownChartData;
function initCrashFreeChartData() {
    return {
        users: {
            seriesName: sessionTerm_1.sessionTerm['crash-free-users'],
            data: [],
            color: chartPalette_1.default[1][0],
            lineStyle: {
                color: chartPalette_1.default[1][0],
            },
        },
        sessions: {
            seriesName: sessionTerm_1.sessionTerm['crash-free-sessions'],
            data: [],
            color: chartPalette_1.default[1][1],
            lineStyle: {
                color: chartPalette_1.default[1][1],
            },
        },
    };
}
exports.initCrashFreeChartData = initCrashFreeChartData;
function initOtherCrashFreeChartData() {
    return tslib_1.__assign(tslib_1.__assign({}, initOtherReleasesChartData()), { users: {
            seriesName: sessionTerm_1.sessionTerm.otherCrashFreeUsers,
            data: [],
            z: 0,
            color: color_1.default(chartPalette_1.default[1][0]).lighten(0.9).alpha(0.9).string(),
            lineStyle: {
                color: chartPalette_1.default[1][0],
                opacity: 0.1,
            },
        }, sessions: {
            seriesName: sessionTerm_1.sessionTerm.otherCrashFreeSessions,
            data: [],
            z: 0,
            color: color_1.default(chartPalette_1.default[1][1]).lighten(0.5).alpha(0.9).string(),
            lineStyle: {
                color: chartPalette_1.default[1][1],
                opacity: 0.3,
            },
        } });
}
exports.initOtherCrashFreeChartData = initOtherCrashFreeChartData;
function initSessionDurationChartData() {
    return {
        0: {
            seriesName: sessionTerm_1.sessionTerm.duration,
            data: [],
            color: chartPalette_1.default[0][0],
            areaStyle: {
                color: chartPalette_1.default[0][0],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initSessionDurationChartData = initSessionDurationChartData;
function initOtherSessionDurationChartData() {
    return {
        0: {
            seriesName: sessionTerm_1.sessionTerm.otherReleases,
            data: [],
            z: 0,
            color: color_1.default(chartPalette_1.default[0][0]).alpha(0.4).string(),
            areaStyle: {
                color: chartPalette_1.default[0][0],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initOtherSessionDurationChartData = initOtherSessionDurationChartData;
// this series will never be filled with data - we use it to act as an alias in legend (we don't display other healthy, other crashes, etc. there)
// if you click on it, we toggle all "other" series (other healthy, other crashed, ...)
function initOtherReleasesChartData() {
    return {
        otherReleases: {
            seriesName: sessionTerm_1.sessionTerm.otherReleases,
            data: [],
            color: color_1.default(chartPalette_1.default[0][0]).alpha(0.4).string(),
        },
    };
}
function isOtherSeries(series) {
    return [
        sessionTerm_1.sessionTerm.otherCrashed,
        sessionTerm_1.sessionTerm.otherAbnormal,
        sessionTerm_1.sessionTerm.otherErrored,
        sessionTerm_1.sessionTerm.otherHealthy,
        sessionTerm_1.sessionTerm.otherCrashFreeUsers,
        sessionTerm_1.sessionTerm.otherCrashFreeSessions,
    ].includes(series.seriesName);
}
exports.isOtherSeries = isOtherSeries;
var seriesOrder = [
    sessionTerm_1.sessionTerm.healthy,
    sessionTerm_1.sessionTerm.errored,
    sessionTerm_1.sessionTerm.crashed,
    sessionTerm_1.sessionTerm.abnormal,
    sessionTerm_1.sessionTerm.otherHealthy,
    sessionTerm_1.sessionTerm.otherErrored,
    sessionTerm_1.sessionTerm.otherCrashed,
    sessionTerm_1.sessionTerm.otherAbnormal,
    sessionTerm_1.sessionTerm.duration,
    sessionTerm_1.sessionTerm['crash-free-sessions'],
    sessionTerm_1.sessionTerm['crash-free-users'],
    sessionTerm_1.sessionTerm.otherCrashFreeSessions,
    sessionTerm_1.sessionTerm.otherCrashFreeUsers,
    sessionTerm_1.sessionTerm.otherReleases,
];
function sortSessionSeries(a, b) {
    return seriesOrder.indexOf(a.seriesName) - seriesOrder.indexOf(b.seriesName);
}
exports.sortSessionSeries = sortSessionSeries;
function getTotalsFromSessionsResponse(_a) {
    var response = _a.response, field = _a.field;
    return response.groups.reduce(function (acc, group) {
        return acc + group.totals[field];
    }, 0);
}
exports.getTotalsFromSessionsResponse = getTotalsFromSessionsResponse;
function fillChartDataFromSessionsResponse(_a) {
    var response = _a.response, field = _a.field, groupBy = _a.groupBy, chartData = _a.chartData, valueFormatter = _a.valueFormatter;
    response.intervals.forEach(function (interval, index) {
        response.groups.forEach(function (group) {
            var value = group.series[field][index];
            chartData[groupBy === null ? 0 : group.by[groupBy]].data.push({
                name: interval,
                value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
            });
        });
    });
    return chartData;
}
exports.fillChartDataFromSessionsResponse = fillChartDataFromSessionsResponse;
function fillCrashFreeChartDataFromSessionsReponse(_a) {
    var response = _a.response, field = _a.field, entity = _a.entity, chartData = _a.chartData;
    response.intervals.forEach(function (interval, index) {
        var _a, _b;
        var intervalTotalSessions = response.groups.reduce(function (acc, group) { return acc + group.series[field][index]; }, 0);
        var intervalCrashedSessions = (_b = (_a = response.groups.find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.series[field][index]) !== null && _b !== void 0 ? _b : 0;
        var crashedSessionsPercent = utils_2.percent(intervalCrashedSessions, intervalTotalSessions);
        chartData[entity].data.push({
            name: interval,
            value: intervalTotalSessions === 0
                ? null
                : utils_3.getCrashFreePercent(100 - crashedSessionsPercent),
        });
    });
    return chartData;
}
exports.fillCrashFreeChartDataFromSessionsReponse = fillCrashFreeChartDataFromSessionsReponse;
//# sourceMappingURL=utils.jsx.map