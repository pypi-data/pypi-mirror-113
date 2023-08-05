Object.defineProperty(exports, "__esModule", { value: true });
exports.getReleaseStoreKey = void 0;
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var organizationActions_1 = tslib_1.__importDefault(require("app/actions/organizationActions"));
var releaseActions_1 = tslib_1.__importDefault(require("app/actions/releaseActions"));
var getReleaseStoreKey = function (projectSlug, releaseVersion) {
    return "" + projectSlug + releaseVersion;
};
exports.getReleaseStoreKey = getReleaseStoreKey;
var ReleaseStoreConfig = {
    state: {
        orgSlug: undefined,
        release: new Map(),
        releaseLoading: new Map(),
        releaseError: new Map(),
        deploys: new Map(),
        deploysLoading: new Map(),
        deploysError: new Map(),
    },
    listenables: releaseActions_1.default,
    init: function () {
        this.listenTo(organizationActions_1.default.update, this.updateOrganization);
        this.reset();
    },
    reset: function () {
        this.state = {
            orgSlug: undefined,
            release: new Map(),
            releaseLoading: new Map(),
            releaseError: new Map(),
            deploys: new Map(),
            deploysLoading: new Map(),
            deploysError: new Map(),
        };
        this.trigger(this.state);
    },
    updateOrganization: function (org) {
        this.reset();
        this.state.orgSlug = org.slug;
        this.trigger(this.state);
    },
    loadRelease: function (orgSlug, projectSlug, releaseVersion) {
        var _a, _b;
        // Wipe entire store if the user switched organizations
        if (!this.orgSlug || this.orgSlug !== orgSlug) {
            this.reset();
            this.orgSlug = orgSlug;
        }
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, releaseLoading = _c.releaseLoading, releaseError = _c.releaseError, state = tslib_1.__rest(_c, ["releaseLoading", "releaseError"]);
        this.state = tslib_1.__assign(tslib_1.__assign({}, state), { releaseLoading: tslib_1.__assign(tslib_1.__assign({}, releaseLoading), (_a = {}, _a[releaseKey] = true, _a)), releaseError: tslib_1.__assign(tslib_1.__assign({}, releaseError), (_b = {}, _b[releaseKey] = undefined, _b)) });
        this.trigger(this.state);
    },
    loadReleaseError: function (projectSlug, releaseVersion, error) {
        var _a, _b;
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, releaseLoading = _c.releaseLoading, releaseError = _c.releaseError, state = tslib_1.__rest(_c, ["releaseLoading", "releaseError"]);
        this.state = tslib_1.__assign(tslib_1.__assign({}, state), { releaseLoading: tslib_1.__assign(tslib_1.__assign({}, releaseLoading), (_a = {}, _a[releaseKey] = false, _a)), releaseError: tslib_1.__assign(tslib_1.__assign({}, releaseError), (_b = {}, _b[releaseKey] = error, _b)) });
        this.trigger(this.state);
    },
    loadReleaseSuccess: function (projectSlug, releaseVersion, data) {
        var _a, _b, _c;
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        var _d = this.state, release = _d.release, releaseLoading = _d.releaseLoading, releaseError = _d.releaseError, state = tslib_1.__rest(_d, ["release", "releaseLoading", "releaseError"]);
        this.state = tslib_1.__assign(tslib_1.__assign({}, state), { release: tslib_1.__assign(tslib_1.__assign({}, release), (_a = {}, _a[releaseKey] = data, _a)), releaseLoading: tslib_1.__assign(tslib_1.__assign({}, releaseLoading), (_b = {}, _b[releaseKey] = false, _b)), releaseError: tslib_1.__assign(tslib_1.__assign({}, releaseError), (_c = {}, _c[releaseKey] = undefined, _c)) });
        this.trigger(this.state);
    },
    loadDeploys: function (orgSlug, projectSlug, releaseVersion) {
        var _a, _b;
        // Wipe entire store if the user switched organizations
        if (!this.orgSlug || this.orgSlug !== orgSlug) {
            this.reset();
            this.orgSlug = orgSlug;
        }
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, deploysLoading = _c.deploysLoading, deploysError = _c.deploysError, state = tslib_1.__rest(_c, ["deploysLoading", "deploysError"]);
        this.state = tslib_1.__assign(tslib_1.__assign({}, state), { deploysLoading: tslib_1.__assign(tslib_1.__assign({}, deploysLoading), (_a = {}, _a[releaseKey] = true, _a)), deploysError: tslib_1.__assign(tslib_1.__assign({}, deploysError), (_b = {}, _b[releaseKey] = undefined, _b)) });
        this.trigger(this.state);
    },
    loadDeploysError: function (projectSlug, releaseVersion, error) {
        var _a, _b;
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, deploysLoading = _c.deploysLoading, deploysError = _c.deploysError, state = tslib_1.__rest(_c, ["deploysLoading", "deploysError"]);
        this.state = tslib_1.__assign(tslib_1.__assign({}, state), { deploysLoading: tslib_1.__assign(tslib_1.__assign({}, deploysLoading), (_a = {}, _a[releaseKey] = false, _a)), deploysError: tslib_1.__assign(tslib_1.__assign({}, deploysError), (_b = {}, _b[releaseKey] = error, _b)) });
        this.trigger(this.state);
    },
    loadDeploysSuccess: function (projectSlug, releaseVersion, data) {
        var _a, _b, _c;
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        var _d = this.state, deploys = _d.deploys, deploysLoading = _d.deploysLoading, deploysError = _d.deploysError, state = tslib_1.__rest(_d, ["deploys", "deploysLoading", "deploysError"]);
        this.state = tslib_1.__assign(tslib_1.__assign({}, state), { deploys: tslib_1.__assign(tslib_1.__assign({}, deploys), (_a = {}, _a[releaseKey] = data, _a)), deploysLoading: tslib_1.__assign(tslib_1.__assign({}, deploysLoading), (_b = {}, _b[releaseKey] = false, _b)), deploysError: tslib_1.__assign(tslib_1.__assign({}, deploysError), (_c = {}, _c[releaseKey] = undefined, _c)) });
        this.trigger(this.state);
    },
    get: function (projectSlug, releaseVersion) {
        var releaseKey = exports.getReleaseStoreKey(projectSlug, releaseVersion);
        return {
            release: this.state.release[releaseKey],
            releaseLoading: this.state.releaseLoading[releaseKey],
            releaseError: this.state.releaseError[releaseKey],
            deploys: this.state.deploys[releaseKey],
            deploysLoading: this.state.deploysLoading[releaseKey],
            deploysError: this.state.deploysError[releaseKey],
        };
    },
};
var ReleaseStore = reflux_1.default.createStore(ReleaseStoreConfig);
exports.default = ReleaseStore;
//# sourceMappingURL=releaseStore.jsx.map