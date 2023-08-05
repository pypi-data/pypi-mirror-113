Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var preferencesActions_1 = tslib_1.__importDefault(require("../actions/preferencesActions"));
var preferenceStoreConfig = {
    prefs: {},
    init: function () {
        this.reset();
        this.listenTo(preferencesActions_1.default.hideSidebar, this.onHideSidebar);
        this.listenTo(preferencesActions_1.default.showSidebar, this.onShowSidebar);
        this.listenTo(preferencesActions_1.default.loadInitialState, this.loadInitialState);
    },
    getInitialState: function () {
        return this.prefs;
    },
    reset: function () {
        this.prefs = {
            collapsed: false,
        };
    },
    loadInitialState: function (prefs) {
        this.prefs = tslib_1.__assign({}, prefs);
        this.trigger(this.prefs);
    },
    onHideSidebar: function () {
        this.prefs.collapsed = true;
        this.trigger(this.prefs);
    },
    onShowSidebar: function () {
        this.prefs.collapsed = false;
        this.trigger(this.prefs);
    },
};
/**
 * This store is used to hold local user preferences
 * Side-effects (like reading/writing to cookies) are done in associated actionCreators
 */
var PreferenceStore = reflux_1.default.createStore(preferenceStoreConfig);
exports.default = PreferenceStore;
//# sourceMappingURL=preferencesStore.jsx.map