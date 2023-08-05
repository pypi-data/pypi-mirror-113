Object.defineProperty(exports, "__esModule", { value: true });
exports.getReleaseParams = exports.getReleaseBounds = exports.releaseDisplayLabel = exports.isReleaseArchived = exports.getReleaseUnhandledIssuesUrl = exports.getReleaseNewIssuesUrl = exports.displayCrashFreeDiff = exports.displaySessionStatusPercent = exports.getSessionStatusPercent = exports.displayCrashFreePercent = exports.getCrashFreePercent = exports.roundDuration = exports.CRASH_FREE_DECIMAL_THRESHOLD = void 0;
var tslib_1 = require("tslib");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var round_1 = tslib_1.__importDefault(require("lodash/round"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_1 = require("app/views/issueList/utils");
var utils_2 = require("../list/utils");
exports.CRASH_FREE_DECIMAL_THRESHOLD = 95;
var roundDuration = function (seconds) {
    return round_1.default(seconds, seconds > 60 ? 0 : 3);
};
exports.roundDuration = roundDuration;
var getCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = exports.CRASH_FREE_DECIMAL_THRESHOLD; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    return round_1.default(percent, percent > decimalThreshold ? decimalPlaces : 0);
};
exports.getCrashFreePercent = getCrashFreePercent;
var displayCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = exports.CRASH_FREE_DECIMAL_THRESHOLD; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    if (isNaN(percent)) {
        return '\u2015';
    }
    if (percent < 1 && percent > 0) {
        return "<1%";
    }
    var rounded = exports.getCrashFreePercent(percent, decimalThreshold, decimalPlaces).toLocaleString();
    return rounded + "%";
};
exports.displayCrashFreePercent = displayCrashFreePercent;
var getSessionStatusPercent = function (percent) {
    return round_1.default(percent, 3);
};
exports.getSessionStatusPercent = getSessionStatusPercent;
var displaySessionStatusPercent = function (percent) {
    return exports.getSessionStatusPercent(percent).toLocaleString() + "%";
};
exports.displaySessionStatusPercent = displaySessionStatusPercent;
var displayCrashFreeDiff = function (diffPercent, crashFreePercent) {
    return Math.abs(round_1.default(diffPercent, crashFreePercent && crashFreePercent > exports.CRASH_FREE_DECIMAL_THRESHOLD ? 3 : 0)).toLocaleString() + "%";
};
exports.displayCrashFreeDiff = displayCrashFreeDiff;
var getReleaseNewIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            // we are resetting time selector because releases' new issues count doesn't take time selector into account
            statsPeriod: undefined,
            start: undefined,
            end: undefined,
            query: new tokenizeSearch_1.QueryResults(["firstRelease:" + version]).formatString(),
            sort: utils_1.IssueSortOptions.FREQ,
        },
    };
};
exports.getReleaseNewIssuesUrl = getReleaseNewIssuesUrl;
var getReleaseUnhandledIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            query: new tokenizeSearch_1.QueryResults([
                "release:" + version,
                'error.unhandled:true',
            ]).formatString(),
            sort: utils_1.IssueSortOptions.FREQ,
        },
    };
};
exports.getReleaseUnhandledIssuesUrl = getReleaseUnhandledIssuesUrl;
var isReleaseArchived = function (release) {
    return release.status === types_1.ReleaseStatus.Archived;
};
exports.isReleaseArchived = isReleaseArchived;
function releaseDisplayLabel(displayOption, count) {
    if (displayOption === utils_2.DisplayOption.USERS) {
        return locale_1.tn('user', 'users', count);
    }
    return locale_1.tn('session', 'sessions', count);
}
exports.releaseDisplayLabel = releaseDisplayLabel;
function getReleaseBounds(release) {
    var _a;
    var _b = release || {}, lastEvent = _b.lastEvent, currentProjectMeta = _b.currentProjectMeta, dateCreated = _b.dateCreated;
    var sessionsUpperBound = (currentProjectMeta || {}).sessionsUpperBound;
    return {
        releaseStart: dateCreated,
        releaseEnd: (_a = (moment_1.default(sessionsUpperBound).isAfter(lastEvent) ? sessionsUpperBound : lastEvent)) !== null && _a !== void 0 ? _a : moment_1.default().utc().format(),
    };
}
exports.getReleaseBounds = getReleaseBounds;
// these options are here only temporarily while we still support older and newer release details page
function getReleaseParams(_a) {
    var location = _a.location, releaseBounds = _a.releaseBounds, defaultStatsPeriod = _a.defaultStatsPeriod, allowEmptyPeriod = _a.allowEmptyPeriod;
    var params = getParams_1.getParams(pick_1.default(location.query, tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM))), tslib_1.__read(Object.values(globalSelectionHeader_1.PAGE_URL_PARAM))), [
        'cursor',
    ])), {
        allowAbsolutePageDatetime: true,
        defaultStatsPeriod: defaultStatsPeriod,
        allowEmptyPeriod: allowEmptyPeriod,
    });
    if (!Object.keys(params).some(function (param) {
        return [globalSelectionHeader_1.URL_PARAM.START, globalSelectionHeader_1.URL_PARAM.END, globalSelectionHeader_1.URL_PARAM.UTC, globalSelectionHeader_1.URL_PARAM.PERIOD].includes(param);
    })) {
        params[globalSelectionHeader_1.URL_PARAM.START] = releaseBounds.releaseStart;
        params[globalSelectionHeader_1.URL_PARAM.END] = releaseBounds.releaseEnd;
    }
    return params;
}
exports.getReleaseParams = getReleaseParams;
//# sourceMappingURL=index.jsx.map