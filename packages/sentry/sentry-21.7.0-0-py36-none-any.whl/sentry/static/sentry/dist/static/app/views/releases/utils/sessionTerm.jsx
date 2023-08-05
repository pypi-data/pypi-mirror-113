var _a, _b, _c, _d;
Object.defineProperty(exports, "__esModule", { value: true });
exports.getSessionTermDescription = exports.desktopTermDescriptions = exports.mobileTermsDescription = exports.commonTermsDescription = exports.sessionTerm = exports.SessionTerm = void 0;
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var SessionTerm;
(function (SessionTerm) {
    SessionTerm["CRASHES"] = "crashes";
    SessionTerm["CRASHED"] = "crashed";
    SessionTerm["ABNORMAL"] = "abnormal";
    SessionTerm["CRASH_FREE"] = "crashFree";
    SessionTerm["CRASH_FREE_USERS"] = "crash-free-users";
    SessionTerm["CRASH_FREE_SESSIONS"] = "crash-free-sessions";
    SessionTerm["HEALTHY"] = "healthy";
    SessionTerm["ERRORED"] = "errored";
    SessionTerm["UNHANDLED"] = "unhandled";
    SessionTerm["STABILITY"] = "stability";
    SessionTerm["ADOPTION"] = "adoption";
})(SessionTerm = exports.SessionTerm || (exports.SessionTerm = {}));
exports.sessionTerm = (_a = {},
    _a[SessionTerm.CRASHES] = locale_1.t('Crashes'),
    _a[SessionTerm.CRASHED] = locale_1.t('Crashed'),
    _a[SessionTerm.ABNORMAL] = locale_1.t('Abnormal'),
    _a[SessionTerm.CRASH_FREE_USERS] = locale_1.t('Crash Free Users'),
    _a[SessionTerm.CRASH_FREE_SESSIONS] = locale_1.t('Crash Free Sessions'),
    _a[SessionTerm.HEALTHY] = locale_1.t('Healthy'),
    _a[SessionTerm.ERRORED] = locale_1.t('Errored'),
    _a[SessionTerm.UNHANDLED] = locale_1.t('Unhandled'),
    _a[SessionTerm.ADOPTION] = locale_1.t('Adoption'),
    _a.duration = locale_1.t('Session Duration'),
    _a.otherCrashed = locale_1.t('Other Crashed'),
    _a.otherAbnormal = locale_1.t('Other Abnormal'),
    _a.otherErrored = locale_1.t('Other Errored'),
    _a.otherHealthy = locale_1.t('Other Healthy'),
    _a.otherCrashFreeUsers = locale_1.t('Other Crash Free Users'),
    _a.otherCrashFreeSessions = locale_1.t('Other Crash Free Sessions'),
    _a.otherReleases = locale_1.t('Other Releases'),
    _a);
// This should never be used directly (except in tests)
exports.commonTermsDescription = (_b = {},
    _b[SessionTerm.CRASHES] = locale_1.t('Number of sessions with a crashed state'),
    _b[SessionTerm.CRASH_FREE] = locale_1.t('Percentage of sessions/users who did not experience a crash.'),
    _b[SessionTerm.CRASH_FREE_USERS] = locale_1.t('Percentage of unique users with non-crashed sessions'),
    _b[SessionTerm.CRASH_FREE_SESSIONS] = locale_1.t('Percentage of non-crashed sessions'),
    _b[SessionTerm.STABILITY] = locale_1.t('The percentage of crash free sessions.'),
    _b[SessionTerm.ADOPTION] = locale_1.t('Adoption compares the sessions or users of a release with the total sessions or users for this project in the last 24 hours.'),
    _b);
// This should never be used directly (except in tests)
exports.mobileTermsDescription = (_c = {},
    _c[SessionTerm.CRASHED] = locale_1.t('The process was terminated due to an unhandled exception or a request to the server that ended with an error'),
    _c[SessionTerm.CRASH_FREE_SESSIONS] = locale_1.t('Percentage of non-crashed sessions'),
    _c[SessionTerm.ABNORMAL] = locale_1.t('An unknown session exit. Like due to loss of power or killed by the operating system'),
    _c[SessionTerm.HEALTHY] = locale_1.t('A session without errors'),
    _c[SessionTerm.ERRORED] = locale_1.t('A session with errors'),
    _c[SessionTerm.UNHANDLED] = locale_1.t('Not handled by user code'),
    _c);
// This should never be used directly (except in tests)
exports.desktopTermDescriptions = (_d = {
        crashed: locale_1.t('The application crashed with a hard crash (eg. segfault)')
    },
    _d[SessionTerm.ABNORMAL] = locale_1.t('The application did not properly end the session, for example, due to force-quit'),
    _d[SessionTerm.HEALTHY] = locale_1.t('The application exited normally and did not observe any errors'),
    _d[SessionTerm.ERRORED] = locale_1.t('The application exited normally but observed error events while running'),
    _d[SessionTerm.UNHANDLED] = locale_1.t('The application crashed with a hard crash'),
    _d);
function getTermDescriptions(platform) {
    var _a, _b, _c, _d, _e, _f;
    var technology = platform === 'react-native' ||
        platform === 'java-spring' ||
        platform === 'apple-ios' ||
        platform === 'dotnet-aspnetcore'
        ? platform
        : platform === null || platform === void 0 ? void 0 : platform.split('-')[0];
    switch (technology) {
        case 'dotnet':
        case 'java':
            return tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), exports.mobileTermsDescription);
        case 'java-spring':
        case 'dotnet-aspnetcore':
            return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), exports.mobileTermsDescription), (_a = {}, _a[SessionTerm.CRASHES] = locale_1.t('A request that resulted in an unhandled exception and hence a Server Error response'), _a));
        case 'android':
        case 'cordova':
        case 'react-native':
        case 'flutter':
            return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), exports.mobileTermsDescription), (_b = {}, _b[SessionTerm.CRASHED] = locale_1.t('An unhandled exception that resulted in the application crashing'), _b));
        case 'apple': {
            return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), exports.mobileTermsDescription), (_c = {}, _c[SessionTerm.CRASHED] = locale_1.t('An error that resulted in the application crashing'), _c));
        }
        case 'node':
        case 'javascript':
            return tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), (_d = {}, _d[SessionTerm.CRASHED] = locale_1.t('During the session an unhandled global error/promise rejection occurred.'), _d[SessionTerm.ABNORMAL] = locale_1.t('Non applicable for Javascript.'), _d[SessionTerm.HEALTHY] = locale_1.t('No errors were captured during session life-time.'), _d[SessionTerm.ERRORED] = locale_1.t('During the session at least one handled error occurred.'), _d[SessionTerm.UNHANDLED] = "An error was captured by the global 'onerror' or 'onunhandledrejection' handler.", _d));
        case 'apple-ios':
        case 'minidump':
        case 'native':
            return tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), exports.desktopTermDescriptions);
        case 'rust':
            return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), exports.desktopTermDescriptions), (_e = {}, _e[SessionTerm.CRASHED] = locale_1.t('The application had an unrecoverable error (a panic)'), _e));
        default:
            return tslib_1.__assign(tslib_1.__assign({}, exports.commonTermsDescription), (_f = {}, _f[SessionTerm.CRASHED] = locale_1.t('Number of users who experienced an unhandled error'), _f[SessionTerm.ABNORMAL] = locale_1.t('An unknown session exit'), _f[SessionTerm.HEALTHY] = exports.mobileTermsDescription.healthy, _f[SessionTerm.ERRORED] = exports.mobileTermsDescription.errored, _f[SessionTerm.UNHANDLED] = exports.mobileTermsDescription.unhandled, _f));
    }
}
function getSessionTermDescription(term, platform) {
    return getTermDescriptions(platform)[term];
}
exports.getSessionTermDescription = getSessionTermDescription;
//# sourceMappingURL=sessionTerm.jsx.map