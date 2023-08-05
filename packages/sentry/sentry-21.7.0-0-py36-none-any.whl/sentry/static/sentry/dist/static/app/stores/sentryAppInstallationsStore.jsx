Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var SentryAppInstallationStore = reflux_1.default.createStore({
    init: function () {
        this.items = [];
    },
    getInitialState: function () {
        return this.items;
    },
    load: function (items) {
        this.items = items;
        this.trigger(items);
    },
    get: function (uuid) {
        var items = this.items;
        return items.find(function (item) { return item.uuid === uuid; });
    },
    getAll: function () {
        return this.items;
    },
});
exports.default = SentryAppInstallationStore;
//# sourceMappingURL=sentryAppInstallationsStore.jsx.map