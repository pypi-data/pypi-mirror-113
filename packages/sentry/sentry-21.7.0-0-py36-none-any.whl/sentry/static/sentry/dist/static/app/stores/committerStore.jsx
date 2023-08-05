Object.defineProperty(exports, "__esModule", { value: true });
exports.getCommitterStoreKey = exports.CommitterStoreConfig = void 0;
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var committerActions_1 = tslib_1.__importDefault(require("app/actions/committerActions"));
exports.CommitterStoreConfig = {
    listenables: committerActions_1.default,
    state: {},
    init: function () {
        this.reset();
    },
    reset: function () {
        this.state = {};
        this.trigger(this.state);
    },
    load: function (orgSlug, projectSlug, eventId) {
        var _a;
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), (_a = {}, _a[key] = {
            committers: undefined,
            committersLoading: true,
            committersError: undefined,
        }, _a));
        this.trigger(this.state);
    },
    loadError: function (orgSlug, projectSlug, eventId, err) {
        var _a;
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), (_a = {}, _a[key] = {
            committers: undefined,
            committersLoading: false,
            committersError: err,
        }, _a));
        this.trigger(this.state);
    },
    loadSuccess: function (orgSlug, projectSlug, eventId, data) {
        var _a;
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), (_a = {}, _a[key] = {
            committers: data,
            committersLoading: false,
            committersError: undefined,
        }, _a));
        this.trigger(this.state);
    },
    get: function (orgSlug, projectSlug, eventId) {
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        return tslib_1.__assign({}, this.state[key]);
    },
};
function getCommitterStoreKey(orgSlug, projectSlug, eventId) {
    return orgSlug + " " + projectSlug + " " + eventId;
}
exports.getCommitterStoreKey = getCommitterStoreKey;
var CommitterStore = reflux_1.default.createStore(exports.CommitterStoreConfig);
exports.default = CommitterStore;
//# sourceMappingURL=committerStore.jsx.map