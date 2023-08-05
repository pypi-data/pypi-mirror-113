Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var formSearchActions_1 = tslib_1.__importDefault(require("app/actions/formSearchActions"));
/**
 * Store for "form" searches, but probably will include more
 */
var formSearchStoreConfig = {
    searchMap: null,
    init: function () {
        this.reset();
        this.listenTo(formSearchActions_1.default.loadSearchMap, this.onLoadSearchMap);
    },
    get: function () {
        return this.searchMap;
    },
    reset: function () {
        // `null` means it hasn't been loaded yet
        this.searchMap = null;
    },
    /**
     * Adds to search map
     */
    onLoadSearchMap: function (searchMap) {
        // Only load once
        if (this.searchMap !== null) {
            return;
        }
        this.searchMap = searchMap;
        this.trigger(this.searchMap);
    },
};
var FormSearchStore = reflux_1.default.createStore(formSearchStoreConfig);
exports.default = FormSearchStore;
//# sourceMappingURL=formSearchStore.jsx.map