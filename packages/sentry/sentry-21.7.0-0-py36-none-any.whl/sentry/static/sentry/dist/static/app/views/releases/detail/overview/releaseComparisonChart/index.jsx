Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var styles_1 = require("app/components/charts/styles");
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var utils_1 = require("app/utils");
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var sessions_1 = require("app/utils/sessions");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_2 = require("app/views/releases/utils");
var utils_3 = require("../../utils");
var utils_4 = require("../chart/utils");
var releaseEventsChart_1 = tslib_1.__importDefault(require("./releaseEventsChart"));
var releaseSessionsChart_1 = tslib_1.__importDefault(require("./releaseSessionsChart"));
function ReleaseComparisonChart(_a) {
    var release = _a.release, project = _a.project, releaseSessions = _a.releaseSessions, allSessions = _a.allSessions, platform = _a.platform, location = _a.location, loading = _a.loading, reloading = _a.reloading, errored = _a.errored, theme = _a.theme, api = _a.api, organization = _a.organization;
    var _b = tslib_1.__read(react_1.useState(null), 2), eventsTotals = _b[0], setEventsTotals = _b[1];
    var _c = utils_2.getReleaseParams({
        location: location,
        releaseBounds: utils_2.getReleaseBounds(release),
        defaultStatsPeriod: constants_1.DEFAULT_STATS_PERIOD,
        allowEmptyPeriod: true,
    }), period = _c.statsPeriod, start = _c.start, end = _c.end, utc = _c.utc;
    react_1.useEffect(function () {
        fetchEventsTotals();
    }, [period, start, end, organization.slug, location]);
    function fetchEventsTotals() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var url, commonQuery, _a, releaseTransactionTotals, allTransactionTotals, releaseErrorTotals, allErrorTotals, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        url = "/organizations/" + organization.slug + "/eventsv2/";
                        commonQuery = tslib_1.__assign({ environment: queryString_1.decodeList(location.query.environment), project: queryString_1.decodeList(location.query.project), start: start, end: end }, (period ? { statsPeriod: period } : {}));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['failure_rate()', 'count()'], query: new tokenizeSearch_1.QueryResults([
                                            'event.type:transaction',
                                            "release:" + release.version,
                                        ]).formatString() }, commonQuery),
                                }),
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['failure_rate()', 'count()'], query: new tokenizeSearch_1.QueryResults(['event.type:transaction']).formatString() }, commonQuery),
                                }),
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['count()'], query: new tokenizeSearch_1.QueryResults([
                                            'event.type:error',
                                            "release:" + release.version,
                                        ]).formatString() }, commonQuery),
                                }),
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['count()'], query: new tokenizeSearch_1.QueryResults(['event.type:error']).formatString() }, commonQuery),
                                }),
                            ])];
                    case 2:
                        _a = tslib_1.__read.apply(void 0, [_b.sent(), 4]), releaseTransactionTotals = _a[0], allTransactionTotals = _a[1], releaseErrorTotals = _a[2], allErrorTotals = _a[3];
                        setEventsTotals({
                            allErrorCount: allErrorTotals.data[0].count,
                            releaseErrorCount: releaseErrorTotals.data[0].count,
                            allTransactionCount: allTransactionTotals.data[0].count,
                            releaseTransactionCount: releaseTransactionTotals.data[0].count,
                            releaseFailureRate: releaseTransactionTotals.data[0].failure_rate,
                            allFailureRate: allTransactionTotals.data[0].failure_rate,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        setEventsTotals(null);
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    var activeChart = queryString_1.decodeScalar(location.query.chart, types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS);
    var releaseCrashFreeSessions = sessions_1.getCrashFreeRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS);
    var allCrashFreeSessions = sessions_1.getCrashFreeRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS);
    var diffCrashFreeSessions = utils_1.defined(releaseCrashFreeSessions) && utils_1.defined(allCrashFreeSessions)
        ? releaseCrashFreeSessions - allCrashFreeSessions
        : null;
    var releaseHealthySessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY);
    var allHealthySessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY);
    var diffHealthySessions = utils_1.defined(releaseHealthySessions) && utils_1.defined(allHealthySessions)
        ? releaseHealthySessions - allHealthySessions
        : null;
    var releaseAbnormalSessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL);
    var allAbnormalSessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL);
    var diffAbnormalSessions = utils_1.defined(releaseAbnormalSessions) && utils_1.defined(allAbnormalSessions)
        ? releaseAbnormalSessions - allAbnormalSessions
        : null;
    var releaseErroredSessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED);
    var allErroredSessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED);
    var diffErroredSessions = utils_1.defined(releaseErroredSessions) && utils_1.defined(allErroredSessions)
        ? releaseErroredSessions - allErroredSessions
        : null;
    var releaseCrashedSessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED);
    var allCrashedSessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED);
    var diffCrashedSessions = utils_1.defined(releaseCrashedSessions) && utils_1.defined(allCrashedSessions)
        ? releaseCrashedSessions - allCrashedSessions
        : null;
    var releaseCrashFreeUsers = sessions_1.getCrashFreeRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    var allCrashFreeUsers = sessions_1.getCrashFreeRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS);
    var diffCrashFreeUsers = utils_1.defined(releaseCrashFreeUsers) && utils_1.defined(allCrashFreeUsers)
        ? releaseCrashFreeUsers - allCrashFreeUsers
        : null;
    var releaseHealthyUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY);
    var allHealthyUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY);
    var diffHealthyUsers = utils_1.defined(releaseHealthyUsers) && utils_1.defined(allHealthyUsers)
        ? releaseHealthyUsers - allHealthyUsers
        : null;
    var releaseAbnormalUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL);
    var allAbnormalUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL);
    var diffAbnormalUsers = utils_1.defined(releaseAbnormalUsers) && utils_1.defined(allAbnormalUsers)
        ? releaseAbnormalUsers - allAbnormalUsers
        : null;
    var releaseErroredUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED);
    var allErroredUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED);
    var diffErroredUsers = utils_1.defined(releaseErroredUsers) && utils_1.defined(allErroredUsers)
        ? releaseErroredUsers - allErroredUsers
        : null;
    var releaseCrashedUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED);
    var allCrashedUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED);
    var diffCrashedUsers = utils_1.defined(releaseCrashedUsers) && utils_1.defined(allCrashedUsers)
        ? releaseCrashedUsers - allCrashedUsers
        : null;
    var releaseSessionsCount = sessions_1.getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS);
    var allSessionsCount = sessions_1.getCount(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS);
    var releaseUsersCount = sessions_1.getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    var allUsersCount = sessions_1.getCount(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS);
    var diffFailure = (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate) && (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
        ? eventsTotals.releaseFailureRate - eventsTotals.allFailureRate
        : null;
    // TODO(release-comparison): conditional based on sessions/transactions/discover existence
    var charts = [
        {
            type: types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS,
            thisRelease: utils_1.defined(releaseCrashFreeSessions)
                ? utils_2.displayCrashFreePercent(releaseCrashFreeSessions)
                : null,
            allReleases: utils_1.defined(allCrashFreeSessions)
                ? utils_2.displayCrashFreePercent(allCrashFreeSessions)
                : null,
            diff: utils_1.defined(diffCrashFreeSessions)
                ? utils_2.displayCrashFreeDiff(diffCrashFreeSessions, releaseCrashFreeSessions)
                : null,
            diffDirection: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'green300'
                    : 'red300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS,
            thisRelease: utils_1.defined(releaseHealthySessions)
                ? utils_2.displaySessionStatusPercent(releaseHealthySessions)
                : null,
            allReleases: utils_1.defined(allHealthySessions)
                ? utils_2.displaySessionStatusPercent(allHealthySessions)
                : null,
            diff: utils_1.defined(diffHealthySessions)
                ? utils_2.displaySessionStatusPercent(diffHealthySessions)
                : null,
            diffDirection: diffHealthySessions
                ? diffHealthySessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffHealthySessions
                ? diffHealthySessions > 0
                    ? 'green300'
                    : 'red300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS,
            thisRelease: utils_1.defined(releaseAbnormalSessions)
                ? utils_2.displaySessionStatusPercent(releaseAbnormalSessions)
                : null,
            allReleases: utils_1.defined(allAbnormalSessions)
                ? utils_2.displaySessionStatusPercent(allAbnormalSessions)
                : null,
            diff: utils_1.defined(diffAbnormalSessions)
                ? utils_2.displaySessionStatusPercent(diffAbnormalSessions)
                : null,
            diffDirection: diffAbnormalSessions
                ? diffAbnormalSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffAbnormalSessions
                ? diffAbnormalSessions > 0
                    ? 'red300'
                    : 'green300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.ERRORED_SESSIONS,
            thisRelease: utils_1.defined(releaseErroredSessions)
                ? utils_2.displaySessionStatusPercent(releaseErroredSessions)
                : null,
            allReleases: utils_1.defined(allErroredSessions)
                ? utils_2.displaySessionStatusPercent(allErroredSessions)
                : null,
            diff: utils_1.defined(diffErroredSessions)
                ? utils_2.displaySessionStatusPercent(diffErroredSessions)
                : null,
            diffDirection: diffErroredSessions
                ? diffErroredSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffErroredSessions
                ? diffErroredSessions > 0
                    ? 'red300'
                    : 'green300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.CRASHED_SESSIONS,
            thisRelease: utils_1.defined(releaseCrashedSessions)
                ? utils_2.displaySessionStatusPercent(releaseCrashedSessions)
                : null,
            allReleases: utils_1.defined(allCrashedSessions)
                ? utils_2.displaySessionStatusPercent(allCrashedSessions)
                : null,
            diff: utils_1.defined(diffCrashedSessions)
                ? utils_2.displaySessionStatusPercent(diffCrashedSessions)
                : null,
            diffDirection: diffCrashedSessions
                ? diffCrashedSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashedSessions
                ? diffCrashedSessions > 0
                    ? 'red300'
                    : 'green300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.CRASH_FREE_USERS,
            thisRelease: utils_1.defined(releaseCrashFreeUsers)
                ? utils_2.displayCrashFreePercent(releaseCrashFreeUsers)
                : null,
            allReleases: utils_1.defined(allCrashFreeUsers)
                ? utils_2.displayCrashFreePercent(allCrashFreeUsers)
                : null,
            diff: utils_1.defined(diffCrashFreeUsers)
                ? utils_2.displayCrashFreeDiff(diffCrashFreeUsers, releaseCrashFreeUsers)
                : null,
            diffDirection: diffCrashFreeUsers ? (diffCrashFreeUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffCrashFreeUsers
                ? diffCrashFreeUsers > 0
                    ? 'green300'
                    : 'red300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.HEALTHY_USERS,
            thisRelease: utils_1.defined(releaseHealthyUsers)
                ? utils_2.displaySessionStatusPercent(releaseHealthyUsers)
                : null,
            allReleases: utils_1.defined(allHealthyUsers)
                ? utils_2.displaySessionStatusPercent(allHealthyUsers)
                : null,
            diff: utils_1.defined(diffHealthyUsers)
                ? utils_2.displaySessionStatusPercent(diffHealthyUsers)
                : null,
            diffDirection: diffHealthyUsers ? (diffHealthyUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffHealthyUsers ? (diffHealthyUsers > 0 ? 'green300' : 'red300') : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.ABNORMAL_USERS,
            thisRelease: utils_1.defined(releaseAbnormalUsers)
                ? utils_2.displaySessionStatusPercent(releaseAbnormalUsers)
                : null,
            allReleases: utils_1.defined(allAbnormalUsers)
                ? utils_2.displaySessionStatusPercent(allAbnormalUsers)
                : null,
            diff: utils_1.defined(diffAbnormalUsers)
                ? utils_2.displaySessionStatusPercent(diffAbnormalUsers)
                : null,
            diffDirection: diffAbnormalUsers ? (diffAbnormalUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffAbnormalUsers
                ? diffAbnormalUsers > 0
                    ? 'red300'
                    : 'green300'
                : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.ERRORED_USERS,
            thisRelease: utils_1.defined(releaseErroredUsers)
                ? utils_2.displaySessionStatusPercent(releaseErroredUsers)
                : null,
            allReleases: utils_1.defined(allErroredUsers)
                ? utils_2.displaySessionStatusPercent(allErroredUsers)
                : null,
            diff: utils_1.defined(diffErroredUsers)
                ? utils_2.displaySessionStatusPercent(diffErroredUsers)
                : null,
            diffDirection: diffErroredUsers ? (diffErroredUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffErroredUsers ? (diffErroredUsers > 0 ? 'red300' : 'green300') : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.CRASHED_USERS,
            thisRelease: utils_1.defined(releaseCrashedUsers)
                ? utils_2.displaySessionStatusPercent(releaseCrashedUsers)
                : null,
            allReleases: utils_1.defined(allCrashedUsers)
                ? utils_2.displaySessionStatusPercent(allCrashedUsers)
                : null,
            diff: utils_1.defined(diffCrashedUsers)
                ? utils_2.displaySessionStatusPercent(diffCrashedUsers)
                : null,
            diffDirection: diffCrashedUsers ? (diffCrashedUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffCrashedUsers ? (diffCrashedUsers > 0 ? 'red300' : 'green300') : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.FAILURE_RATE,
            thisRelease: (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate)
                ? formatters_1.formatPercentage(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate)
                : null,
            allReleases: (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
                ? formatters_1.formatPercentage(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
                : null,
            diff: diffFailure ? formatters_1.formatPercentage(Math.abs(diffFailure)) : null,
            diffDirection: diffFailure ? (diffFailure > 0 ? 'up' : 'down') : null,
            diffColor: diffFailure ? (diffFailure > 0 ? 'red300' : 'green300') : null,
        },
        {
            type: types_1.ReleaseComparisonChartType.SESSION_COUNT,
            thisRelease: utils_1.defined(releaseSessionsCount) ? (<count_1.default value={releaseSessionsCount}/>) : null,
            allReleases: utils_1.defined(allSessionsCount) ? <count_1.default value={allSessionsCount}/> : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        },
        {
            type: types_1.ReleaseComparisonChartType.USER_COUNT,
            thisRelease: utils_1.defined(releaseUsersCount) ? (<count_1.default value={releaseUsersCount}/>) : null,
            allReleases: utils_1.defined(allUsersCount) ? <count_1.default value={allUsersCount}/> : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        },
        {
            type: types_1.ReleaseComparisonChartType.ERROR_COUNT,
            thisRelease: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseErrorCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseErrorCount}/>) : null,
            allReleases: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allErrorCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allErrorCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        },
        {
            type: types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
            thisRelease: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseTransactionCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseTransactionCount}/>) : null,
            allReleases: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allTransactionCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allTransactionCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        },
    ];
    function getSeries(chartType) {
        if (!releaseSessions) {
            return {};
        }
        var markLines = utils_3.generateReleaseMarkLines(release, project.slug, theme);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getCrashFreeRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getCrashFreeRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getCrashFreeRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getCrashFreeRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
                return {
                    series: Object.values(utils_4.fillChartDataFromSessionsResponse({
                        response: releaseSessions,
                        field: types_1.SessionField.SESSIONS,
                        groupBy: 'session.status',
                        chartData: utils_4.initSessionsBreakdownChartData(),
                    })),
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.USER_COUNT:
                return {
                    series: Object.values(utils_4.fillChartDataFromSessionsResponse({
                        response: releaseSessions,
                        field: types_1.SessionField.USERS,
                        groupBy: 'session.status',
                        chartData: utils_4.initSessionsBreakdownChartData(),
                    })),
                    markLines: markLines,
                };
            default:
                return {};
        }
    }
    function handleChartChange(chartType) {
        react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { chart: chartType }) }));
    }
    var _d = getSeries(activeChart), series = _d.series, previousSeries = _d.previousSeries, markLines = _d.markLines;
    var chart = charts.find(function (ch) { return ch.type === activeChart; });
    if (errored || !chart) {
        return (<panels_1.Panel>
        <errorPanel_1.default>
          <icons_1.IconWarning color="gray300" size="lg"/>
        </errorPanel_1.default>
      </panels_1.Panel>);
    }
    var chartDiff = chart.diff ? (<Change color={utils_1.defined(chart.diffColor) ? chart.diffColor : undefined}>
      {chart.diff}{' '}
      {utils_1.defined(chart.diffDirection) && (<icons_1.IconArrow direction={chart.diffDirection} size="xs"/>)}
    </Change>) : null;
    return (<react_1.Fragment>
      <ChartPanel>
        <styles_1.ChartContainer>
          {[
            types_1.ReleaseComparisonChartType.ERROR_COUNT,
            types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
            types_1.ReleaseComparisonChartType.FAILURE_RATE,
        ].includes(activeChart) ? (<releaseEventsChart_1.default version={release.version} chartType={activeChart} period={period !== null && period !== void 0 ? period : undefined} start={start} end={end} utc={utc === 'true'} value={chart.thisRelease} diff={chartDiff}/>) : (<releaseSessionsChart_1.default series={tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((series !== null && series !== void 0 ? series : []))), tslib_1.__read((markLines !== null && markLines !== void 0 ? markLines : [])))} previousSeries={previousSeries !== null && previousSeries !== void 0 ? previousSeries : []} chartType={activeChart} platform={platform} period={period !== null && period !== void 0 ? period : undefined} start={start} end={end} utc={utc === 'true'} value={chart.thisRelease} diff={chartDiff} loading={loading} reloading={reloading}/>)}
        </styles_1.ChartContainer>
      </ChartPanel>
      <ChartTable headers={[
            <Cell key="stability" align="left">
            {locale_1.t('Stability')}
          </Cell>,
            <Cell key="releases" align="right">
            {locale_1.t('All Releases')}
          </Cell>,
            <Cell key="release" align="right">
            {locale_1.t('This Release')}
          </Cell>,
            <Cell key="change" align="right">
            {locale_1.t('Change')}
          </Cell>,
        ]}>
        {charts.map(function (_a) {
            var type = _a.type, thisRelease = _a.thisRelease, allReleases = _a.allReleases, diff = _a.diff, diffDirection = _a.diffDirection, diffColor = _a.diffColor;
            return (<react_1.Fragment key={type}>
                <Cell align="left">
                  <ChartToggle htmlFor={type}>
                    <radio_1.default id={type} disabled={false} checked={type === activeChart} onChange={function () { return handleChartChange(type); }}/>
                    {utils_3.releaseComparisonChartLabels[type]}
                  </ChartToggle>
                </Cell>
                <Cell align="right">
                  {loading ? <placeholder_1.default height="20px"/> : allReleases}
                </Cell>
                <Cell align="right">
                  {loading ? <placeholder_1.default height="20px"/> : thisRelease}
                </Cell>
                <Cell align="right">
                  {loading ? (<placeholder_1.default height="20px"/>) : utils_1.defined(diff) ? (<Change color={utils_1.defined(diffColor) ? diffColor : undefined}>
                      {utils_1.defined(diffDirection) && (<icons_1.IconArrow direction={diffDirection} size="xs"/>)}{' '}
                      {diff}
                    </Change>) : (<notAvailable_1.default />)}
                </Cell>
              </react_1.Fragment>);
        })}
      </ChartTable>
    </react_1.Fragment>);
}
var ChartPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom: none;\n  border-bottom-right-radius: 0;\n"], ["\n  margin-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom: none;\n  border-bottom-right-radius: 0;\n"])));
var ChartTable = styled_1.default(panels_1.PanelTable)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr 1fr 1fr;\n  }\n"], ["\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr 1fr 1fr;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var Cell = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: ", ";\n  ", "\n"], ["\n  text-align: ", ";\n  ", "\n"])), function (p) { return p.align; }, overflowEllipsis_1.default);
var ChartToggle = styled_1.default('label')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-weight: 400;\n  margin-bottom: 0;\n  input {\n    flex-shrink: 0;\n    margin-right: ", " !important;\n    &:hover {\n      cursor: pointer;\n    }\n  }\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  font-weight: 400;\n  margin-bottom: 0;\n  input {\n    flex-shrink: 0;\n    margin-right: ", " !important;\n    &:hover {\n      cursor: pointer;\n    }\n  }\n  &:hover {\n    cursor: pointer;\n  }\n"])), space_1.default(1));
var Change = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.color && "color: " + p.theme[p.color]; });
exports.default = react_2.withTheme(ReleaseComparisonChart);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map