Object.defineProperty(exports, "__esModule", { value: true });
exports.restoreRelease = exports.archiveRelease = exports.getReleaseDeploys = exports.getProjectRelease = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var releaseActions_1 = tslib_1.__importDefault(require("app/actions/releaseActions"));
var locale_1 = require("app/locale");
var releaseStore_1 = tslib_1.__importStar(require("app/stores/releaseStore"));
var types_1 = require("app/types");
function getProjectRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    var path = "/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRelease for the same
    // release to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    releaseStore_1.default.state.releaseLoading[releaseStore_1.getReleaseStoreKey(projectSlug, releaseVersion)] =
        true;
    releaseActions_1.default.loadRelease(orgSlug, projectSlug, releaseVersion);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        releaseActions_1.default.loadReleaseSuccess(projectSlug, releaseVersion, res);
    })
        .catch(function (err) {
        // This happens when a Project is not linked to a specific Release
        if (err.status === 404) {
            releaseActions_1.default.loadReleaseSuccess(projectSlug, releaseVersion, null);
            return;
        }
        releaseActions_1.default.loadReleaseError(projectSlug, releaseVersion, err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getRelease-action-creator']);
            Sentry.captureException(err);
        });
    });
}
exports.getProjectRelease = getProjectRelease;
function getReleaseDeploys(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    var path = "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/deploys/";
    // HACK(leedongwei): Same as above
    releaseStore_1.default.state.deploysLoading[releaseStore_1.getReleaseStoreKey(projectSlug, releaseVersion)] =
        true;
    releaseActions_1.default.loadDeploys(orgSlug, projectSlug, releaseVersion);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        releaseActions_1.default.loadDeploysSuccess(projectSlug, releaseVersion, res);
    })
        .catch(function (err) {
        // This happens when a Project is not linked to a specific Release
        if (err.status === 404) {
            releaseActions_1.default.loadDeploysSuccess(projectSlug, releaseVersion, null);
            return;
        }
        releaseActions_1.default.loadDeploysError(projectSlug, releaseVersion, err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getReleaseDeploys-action-creator']);
            Sentry.captureException(err);
        });
    });
}
exports.getReleaseDeploys = getReleaseDeploys;
function archiveRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    releaseActions_1.default.loadRelease(orgSlug, projectSlug, releaseVersion);
    indicator_1.addLoadingMessage(locale_1.t('Archiving Release\u2026'));
    return api
        .requestPromise("/organizations/" + orgSlug + "/releases/", {
        method: 'POST',
        data: {
            status: types_1.ReleaseStatus.Archived,
            projects: [],
            version: releaseVersion,
        },
    })
        .then(function (release) {
        releaseActions_1.default.loadReleaseSuccess(projectSlug, releaseVersion, release);
        indicator_1.addSuccessMessage(locale_1.t('Release was successfully archived.'));
    })
        .catch(function (error) {
        var _a, _b;
        releaseActions_1.default.loadReleaseError(projectSlug, releaseVersion, error);
        indicator_1.addErrorMessage((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : locale_1.t('Release could not be be archived.'));
        throw error;
    });
}
exports.archiveRelease = archiveRelease;
function restoreRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    releaseActions_1.default.loadRelease(orgSlug, projectSlug, releaseVersion);
    indicator_1.addLoadingMessage(locale_1.t('Restoring Release\u2026'));
    return api
        .requestPromise("/organizations/" + orgSlug + "/releases/", {
        method: 'POST',
        data: {
            status: types_1.ReleaseStatus.Active,
            projects: [],
            version: releaseVersion,
        },
    })
        .then(function (release) {
        releaseActions_1.default.loadReleaseSuccess(projectSlug, releaseVersion, release);
        indicator_1.addSuccessMessage(locale_1.t('Release was successfully restored.'));
    })
        .catch(function (error) {
        var _a, _b;
        releaseActions_1.default.loadReleaseError(projectSlug, releaseVersion, error);
        indicator_1.addErrorMessage((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : locale_1.t('Release could not be be restored.'));
        throw error;
    });
}
exports.restoreRelease = restoreRelease;
//# sourceMappingURL=release.jsx.map