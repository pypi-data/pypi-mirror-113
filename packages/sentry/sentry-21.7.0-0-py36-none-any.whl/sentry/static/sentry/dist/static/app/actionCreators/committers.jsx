Object.defineProperty(exports, "__esModule", { value: true });
exports.getCommitters = void 0;
var tslib_1 = require("tslib");
var committerActions_1 = tslib_1.__importDefault(require("app/actions/committerActions"));
var committerStore_1 = tslib_1.__importStar(require("app/stores/committerStore"));
function getCommitters(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, eventId = params.eventId;
    var path = "/projects/" + orgSlug + "/" + projectSlug + "/events/" + eventId + "/committers/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRepo for the same
    // repo to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    var storeKey = committerStore_1.getCommitterStoreKey(orgSlug, projectSlug, eventId);
    committerStore_1.default.state[storeKey] = tslib_1.__assign(tslib_1.__assign({}, committerStore_1.default.state[storeKey]), { committersLoading: true });
    committerActions_1.default.load(orgSlug, projectSlug, eventId);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        committerActions_1.default.loadSuccess(orgSlug, projectSlug, eventId, res.committers);
    })
        .catch(function (err) {
        // NOTE: Do not captureException here as EventFileCommittersEndpoint returns
        // 404 Not Found if the project did not setup Releases or Commits
        committerActions_1.default.loadError(orgSlug, projectSlug, eventId, err);
    });
}
exports.getCommitters = getCommitters;
//# sourceMappingURL=committers.jsx.map