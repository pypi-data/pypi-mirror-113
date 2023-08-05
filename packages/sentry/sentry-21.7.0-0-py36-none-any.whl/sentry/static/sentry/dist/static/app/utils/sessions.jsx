Object.defineProperty(exports, "__esModule", { value: true });
exports.filterSessionsInTimeWindow = exports.getSessionsInterval = exports.getAdoptionSeries = exports.getSessionStatusRateSeries = exports.getCrashFreeRateSeries = exports.getSessionStatusRate = exports.getCrashFreeRate = exports.getCount = void 0;
var tslib_1 = require("tslib");
var compact_1 = tslib_1.__importDefault(require("lodash/compact"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var utils_1 = require("app/components/charts/utils");
var types_1 = require("app/types");
var utils_2 = require("app/utils");
var utils_3 = require("app/views/releases/utils");
function getCount(groups, field) {
    if (groups === void 0) { groups = []; }
    return groups.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
}
exports.getCount = getCount;
function getCrashFreeRate(groups, field) {
    if (groups === void 0) { groups = []; }
    var crashedRate = getSessionStatusRate(groups, field, types_1.SessionStatus.CRASHED);
    return utils_2.defined(crashedRate) ? utils_3.getCrashFreePercent(100 - crashedRate) : null;
}
exports.getCrashFreeRate = getCrashFreeRate;
function getSessionStatusRate(groups, field, status) {
    if (groups === void 0) { groups = []; }
    var totalCount = getCount(groups, field);
    var crashedCount = getCount(groups.filter(function (_a) {
        var by = _a.by;
        return by['session.status'] === status;
    }), field);
    return !utils_2.defined(totalCount) || totalCount === 0
        ? null
        : utils_2.percent(crashedCount !== null && crashedCount !== void 0 ? crashedCount : 0, totalCount !== null && totalCount !== void 0 ? totalCount : 0);
}
exports.getSessionStatusRate = getSessionStatusRate;
function getCrashFreeRateSeries(groups, intervals, field) {
    if (groups === void 0) { groups = []; }
    if (intervals === void 0) { intervals = []; }
    return compact_1.default(intervals.map(function (interval, i) {
        var _a, _b;
        var intervalTotalSessions = groups.reduce(function (acc, group) { return acc + group.series[field][i]; }, 0);
        var intervalCrashedSessions = (_b = (_a = groups.find(function (group) { return group.by['session.status'] === types_1.SessionStatus.CRASHED; })) === null || _a === void 0 ? void 0 : _a.series[field][i]) !== null && _b !== void 0 ? _b : 0;
        var crashedSessionsPercent = utils_2.percent(intervalCrashedSessions, intervalTotalSessions);
        if (intervalTotalSessions === 0) {
            return null;
        }
        return {
            name: interval,
            value: utils_3.getCrashFreePercent(100 - crashedSessionsPercent),
        };
    }));
}
exports.getCrashFreeRateSeries = getCrashFreeRateSeries;
function getSessionStatusRateSeries(groups, intervals, field, status) {
    if (groups === void 0) { groups = []; }
    if (intervals === void 0) { intervals = []; }
    return compact_1.default(intervals.map(function (interval, i) {
        var _a, _b;
        var intervalTotalSessions = groups.reduce(function (acc, group) { return acc + group.series[field][i]; }, 0);
        var intervalStatusSessions = (_b = (_a = groups.find(function (group) { return group.by['session.status'] === status; })) === null || _a === void 0 ? void 0 : _a.series[field][i]) !== null && _b !== void 0 ? _b : 0;
        var statusSessionsPercent = utils_2.percent(intervalStatusSessions, intervalTotalSessions);
        if (intervalTotalSessions === 0) {
            return null;
        }
        return {
            name: interval,
            value: statusSessionsPercent,
        };
    }));
}
exports.getSessionStatusRateSeries = getSessionStatusRateSeries;
function getAdoptionSeries(releaseGroups, allGroups, intervals, field) {
    if (releaseGroups === void 0) { releaseGroups = []; }
    if (allGroups === void 0) { allGroups = []; }
    if (intervals === void 0) { intervals = []; }
    return intervals.map(function (interval, i) {
        var intervalReleaseSessions = releaseGroups.reduce(function (acc, group) { return acc + group.series[field][i]; }, 0);
        var intervalTotalSessions = allGroups.reduce(function (acc, group) { return acc + group.series[field][i]; }, 0);
        var intervalAdoption = utils_2.percent(intervalReleaseSessions, intervalTotalSessions);
        return {
            name: interval,
            value: Math.round(intervalAdoption),
        };
    });
}
exports.getAdoptionSeries = getAdoptionSeries;
function getSessionsInterval(datetimeObj, _a) {
    var _b = _a === void 0 ? {} : _a, highFidelity = _b.highFidelity;
    var diffInMinutes = utils_1.getDiffInMinutes(datetimeObj);
    if (diffInMinutes > utils_1.TWO_WEEKS) {
        return '1d';
    }
    if (diffInMinutes > utils_1.ONE_WEEK) {
        return '6h';
    }
    // limit on backend for sub-hour session resolution is set to six hours
    if (highFidelity && diffInMinutes < 360) {
        if (diffInMinutes <= 30) {
            return '1m';
        }
        return '5m';
    }
    return '1h';
}
exports.getSessionsInterval = getSessionsInterval;
// Sessions API can only round intervals to the closest hour - this is especially problematic when using sub-hour resolution.
// We filter out results that are out of bounds on frontend and recalculate totals.
function filterSessionsInTimeWindow(sessions, start, end) {
    if (!start || !end) {
        return sessions;
    }
    var filteredIndexes = [];
    var intervals = sessions.intervals.filter(function (interval, index) {
        var isBetween = moment_1.default(interval).isBetween(start, end, undefined, '[]');
        if (isBetween) {
            filteredIndexes.push(index);
        }
        return isBetween;
    });
    var groups = sessions.groups.map(function (group) {
        var series = {};
        var totals = {};
        Object.keys(group.series).forEach(function (field) {
            series[field] = group.series[field].filter(function (value, index) {
                var _a;
                var isBetween = filteredIndexes.includes(index);
                if (isBetween) {
                    totals[field] = ((_a = totals[field]) !== null && _a !== void 0 ? _a : 0) + value;
                }
                return isBetween;
            });
        });
        return tslib_1.__assign(tslib_1.__assign({}, group), { series: series, totals: totals });
    });
    return {
        start: intervals[0],
        end: intervals[intervals.length - 1],
        query: sessions.query,
        intervals: intervals,
        groups: groups,
    };
}
exports.filterSessionsInTimeWindow = filterSessionsInTimeWindow;
//# sourceMappingURL=sessions.jsx.map