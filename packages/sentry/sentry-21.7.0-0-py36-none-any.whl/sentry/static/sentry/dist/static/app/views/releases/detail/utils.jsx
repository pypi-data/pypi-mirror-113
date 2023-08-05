var _a, _b, _c;
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateReleaseMarkLines = exports.releaseMarkLinesLabels = exports.releaseComparisonChartHelp = exports.releaseComparisonChartTitles = exports.releaseComparisonChartLabels = exports.getReleaseEventView = exports.getReposToRender = exports.getQuery = exports.getCommitsByRepository = exports.getFilesByRepository = void 0;
var tslib_1 = require("tslib");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var markLine_1 = tslib_1.__importDefault(require("app/components/charts/components/markLine"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var dates_1 = require("app/utils/dates");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var sessionTerm_1 = require("../utils/sessionTerm");
/**
 * Convert list of individual file changes into a per-file summary grouped by repository
 */
function getFilesByRepository(fileList) {
    return fileList.reduce(function (filesByRepository, file) {
        var filename = file.filename, repoName = file.repoName, author = file.author, type = file.type;
        if (!filesByRepository.hasOwnProperty(repoName)) {
            filesByRepository[repoName] = {};
        }
        if (!filesByRepository[repoName].hasOwnProperty(filename)) {
            filesByRepository[repoName][filename] = {
                authors: {},
                types: new Set(),
            };
        }
        if (author.email) {
            filesByRepository[repoName][filename].authors[author.email] = author;
        }
        filesByRepository[repoName][filename].types.add(type);
        return filesByRepository;
    }, {});
}
exports.getFilesByRepository = getFilesByRepository;
/**
 * Convert list of individual commits into a summary grouped by repository
 */
function getCommitsByRepository(commitList) {
    return commitList.reduce(function (commitsByRepository, commit) {
        var _a, _b;
        var repositoryName = (_b = (_a = commit.repository) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : locale_1.t('unknown');
        if (!commitsByRepository.hasOwnProperty(repositoryName)) {
            commitsByRepository[repositoryName] = [];
        }
        commitsByRepository[repositoryName].push(commit);
        return commitsByRepository;
    }, {});
}
exports.getCommitsByRepository = getCommitsByRepository;
function getQuery(_a) {
    var location = _a.location, _b = _a.perPage, perPage = _b === void 0 ? 40 : _b, activeRepository = _a.activeRepository;
    var query = tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM))), ['cursor']))), { per_page: perPage });
    if (!activeRepository) {
        return query;
    }
    return tslib_1.__assign(tslib_1.__assign({}, query), { repo_name: activeRepository.name });
}
exports.getQuery = getQuery;
/**
 * Get repositories to render according to the activeRepository
 */
function getReposToRender(repos, activeRepository) {
    if (!activeRepository) {
        return repos;
    }
    return [activeRepository.name];
}
exports.getReposToRender = getReposToRender;
/**
 * Get high level transaction information for this release
 */
function getReleaseEventView(selection, version, organization) {
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period;
    var apdexField = organization.features.includes('project-transaction-threshold')
        ? 'apdex()'
        : "apdex(" + organization.apdexThreshold + ")";
    var discoverQuery = {
        id: undefined,
        version: 2,
        name: "" + locale_1.t('Release Apdex'),
        fields: [apdexField],
        query: new tokenizeSearch_1.QueryResults([
            "release:" + version,
            'event.type:transaction',
            'count():>0',
        ]).formatString(),
        range: period,
        environment: environments,
        projects: projects,
        start: start ? dates_1.getUtcDateString(start) : undefined,
        end: end ? dates_1.getUtcDateString(end) : undefined,
    };
    return eventView_1.default.fromSavedQuery(discoverQuery);
}
exports.getReleaseEventView = getReleaseEventView;
exports.releaseComparisonChartLabels = (_a = {},
    _a[types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS] = locale_1.t('Crash Free Session Rate'),
    _a[types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS] = locale_1.t('Healthy'),
    _a[types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS] = locale_1.t('Abnormal'),
    _a[types_1.ReleaseComparisonChartType.ERRORED_SESSIONS] = locale_1.t('Errored'),
    _a[types_1.ReleaseComparisonChartType.CRASHED_SESSIONS] = locale_1.t('Crashed Session Rate'),
    _a[types_1.ReleaseComparisonChartType.CRASH_FREE_USERS] = locale_1.t('Crash Free User Rate'),
    _a[types_1.ReleaseComparisonChartType.HEALTHY_USERS] = locale_1.t('Healthy'),
    _a[types_1.ReleaseComparisonChartType.ABNORMAL_USERS] = locale_1.t('Abnormal'),
    _a[types_1.ReleaseComparisonChartType.ERRORED_USERS] = locale_1.t('Errored'),
    _a[types_1.ReleaseComparisonChartType.CRASHED_USERS] = locale_1.t('Crashed User Rate'),
    _a[types_1.ReleaseComparisonChartType.SESSION_COUNT] = locale_1.t('Session Count'),
    _a[types_1.ReleaseComparisonChartType.USER_COUNT] = locale_1.t('User Count'),
    _a[types_1.ReleaseComparisonChartType.ERROR_COUNT] = locale_1.t('Error Count'),
    _a[types_1.ReleaseComparisonChartType.TRANSACTION_COUNT] = locale_1.t('Transaction Count'),
    _a[types_1.ReleaseComparisonChartType.FAILURE_RATE] = locale_1.t('Failure Rate'),
    _a);
exports.releaseComparisonChartTitles = (_b = {},
    _b[types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS] = locale_1.t('Crash Free Session Rate'),
    _b[types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS] = locale_1.t('Healthy Session Rate'),
    _b[types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS] = locale_1.t('Abnormal Session Rate'),
    _b[types_1.ReleaseComparisonChartType.ERRORED_SESSIONS] = locale_1.t('Errored Session Rate'),
    _b[types_1.ReleaseComparisonChartType.CRASHED_SESSIONS] = locale_1.t('Crashed Session Rate'),
    _b[types_1.ReleaseComparisonChartType.CRASH_FREE_USERS] = locale_1.t('Crash Free User Rate'),
    _b[types_1.ReleaseComparisonChartType.HEALTHY_USERS] = locale_1.t('Healthy User Rate'),
    _b[types_1.ReleaseComparisonChartType.ABNORMAL_USERS] = locale_1.t('Abnormal User Rate'),
    _b[types_1.ReleaseComparisonChartType.ERRORED_USERS] = locale_1.t('Errored User Rate'),
    _b[types_1.ReleaseComparisonChartType.CRASHED_USERS] = locale_1.t('Crashed User Rate'),
    _b[types_1.ReleaseComparisonChartType.SESSION_COUNT] = locale_1.t('Session Count'),
    _b[types_1.ReleaseComparisonChartType.USER_COUNT] = locale_1.t('User Count'),
    _b[types_1.ReleaseComparisonChartType.ERROR_COUNT] = locale_1.t('Error Count'),
    _b[types_1.ReleaseComparisonChartType.TRANSACTION_COUNT] = locale_1.t('Transaction Count'),
    _b[types_1.ReleaseComparisonChartType.FAILURE_RATE] = locale_1.t('Failure Rate'),
    _b);
exports.releaseComparisonChartHelp = (_c = {},
    _c[types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS] = sessionTerm_1.commonTermsDescription[sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS],
    _c[types_1.ReleaseComparisonChartType.CRASH_FREE_USERS] = sessionTerm_1.commonTermsDescription[sessionTerm_1.SessionTerm.CRASH_FREE_USERS],
    _c[types_1.ReleaseComparisonChartType.SESSION_COUNT] = locale_1.t('The number of sessions in a given period.'),
    _c[types_1.ReleaseComparisonChartType.USER_COUNT] = locale_1.t('The number of users in a given period.'),
    _c);
function generateReleaseMarkLine(title, position, theme, options) {
    var _a = options || {}, hideLabel = _a.hideLabel, axisIndex = _a.axisIndex;
    return {
        seriesName: title,
        type: 'line',
        data: [{ name: position, value: null }],
        yAxisIndex: axisIndex !== null && axisIndex !== void 0 ? axisIndex : undefined,
        xAxisIndex: axisIndex !== null && axisIndex !== void 0 ? axisIndex : undefined,
        color: theme.gray300,
        markLine: markLine_1.default({
            silent: true,
            lineStyle: { color: theme.gray300, type: 'solid' },
            label: {
                position: 'insideEndBottom',
                formatter: hideLabel ? '' : title,
                font: 'Rubik',
                fontSize: 11,
            },
            data: [
                {
                    xAxis: position,
                },
            ], // TODO(ts): weird echart types
        }),
    };
}
exports.releaseMarkLinesLabels = {
    created: locale_1.t('Release Created'),
    adopted: locale_1.t('Adopted'),
    unadopted: locale_1.t('Unadopted'),
};
function generateReleaseMarkLines(release, projectSlug, theme, options) {
    var _a;
    var adoptionStages = (_a = release.adoptionStages) === null || _a === void 0 ? void 0 : _a[projectSlug];
    var markLines = [
        generateReleaseMarkLine(exports.releaseMarkLinesLabels.created, moment_1.default(release.dateCreated).valueOf(), theme, options),
    ];
    if (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages.adopted) {
        markLines.push(generateReleaseMarkLine(exports.releaseMarkLinesLabels.adopted, moment_1.default(adoptionStages.adopted).valueOf(), theme, options));
    }
    if (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages.unadopted) {
        markLines.push(generateReleaseMarkLine(exports.releaseMarkLinesLabels.unadopted, moment_1.default(adoptionStages.unadopted).valueOf(), theme, options));
    }
    return markLines;
}
exports.generateReleaseMarkLines = generateReleaseMarkLines;
//# sourceMappingURL=utils.jsx.map