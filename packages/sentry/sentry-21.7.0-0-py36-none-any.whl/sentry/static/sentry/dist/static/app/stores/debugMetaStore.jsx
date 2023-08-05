Object.defineProperty(exports, "__esModule", { value: true });
exports.DebugMetaStore = exports.DebugMetaActions = void 0;
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var DebugMetaActions = reflux_1.default.createActions(['updateFilter']);
exports.DebugMetaActions = DebugMetaActions;
var storeConfig = {
    filter: null,
    init: function () {
        this.reset();
        this.listenTo(DebugMetaActions.updateFilter, this.updateFilter);
    },
    reset: function () {
        this.filter = null;
        this.trigger(this.get());
    },
    updateFilter: function (word) {
        this.filter = word;
        this.trigger(this.get());
    },
    get: function () {
        return {
            filter: this.filter,
        };
    },
};
var DebugMetaStore = reflux_1.default.createStore(storeConfig);
exports.DebugMetaStore = DebugMetaStore;
exports.default = DebugMetaStore;
//# sourceMappingURL=debugMetaStore.jsx.map