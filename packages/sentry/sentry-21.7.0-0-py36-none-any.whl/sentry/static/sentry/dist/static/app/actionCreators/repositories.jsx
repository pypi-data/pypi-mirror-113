Object.defineProperty(exports, "__esModule", { value: true });
exports.getRepositories = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var repositoryActions_1 = tslib_1.__importDefault(require("app/actions/repositoryActions"));
var repositoryStore_1 = tslib_1.__importDefault(require("app/stores/repositoryStore"));
function getRepositories(api, params) {
    var orgSlug = params.orgSlug;
    var path = "/organizations/" + orgSlug + "/repos/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRepo for the same
    // repo to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    repositoryStore_1.default.state.repositoriesLoading = true;
    repositoryActions_1.default.loadRepositories(orgSlug);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        repositoryActions_1.default.loadRepositoriesSuccess(res);
    })
        .catch(function (err) {
        repositoryActions_1.default.loadRepositoriesError(err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getRepositories-action-creator']);
            Sentry.captureException(err);
        });
    });
}
exports.getRepositories = getRepositories;
//# sourceMappingURL=repositories.jsx.map