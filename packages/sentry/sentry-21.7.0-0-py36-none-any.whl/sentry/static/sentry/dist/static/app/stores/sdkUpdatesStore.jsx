Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var sdkUpdatesActions_1 = tslib_1.__importDefault(require("app/actions/sdkUpdatesActions"));
var storeConfig = {
    orgSdkUpdates: new Map(),
    init: function () {
        this.listenTo(sdkUpdatesActions_1.default.load, this.onLoadSuccess);
    },
    onLoadSuccess: function (orgSlug, data) {
        this.orgSdkUpdates.set(orgSlug, data);
        this.trigger(this.orgSdkUpdates);
    },
    getUpdates: function (orgSlug) {
        return this.orgSdkUpdates.get(orgSlug);
    },
    isSdkUpdatesLoaded: function (orgSlug) {
        return this.orgSdkUpdates.has(orgSlug);
    },
};
var SdkUpdatesStore = reflux_1.default.createStore(storeConfig);
exports.default = SdkUpdatesStore;
//# sourceMappingURL=sdkUpdatesStore.jsx.map