Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var sentryAppComponentActions_1 = tslib_1.__importDefault(require("app/actions/sentryAppComponentActions"));
var SentryAppComponentsStore = reflux_1.default.createStore({
    init: function () {
        this.items = [];
        this.listenTo(sentryAppComponentActions_1.default.loadComponents, this.onLoadComponents);
    },
    getInitialState: function () {
        return this.items;
    },
    onLoadComponents: function (items) {
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
    getComponentByType: function (type) {
        if (!type) {
            return this.getAll();
        }
        var items = this.items;
        return items.filter(function (item) { return item.type === type; });
    },
});
exports.default = SentryAppComponentsStore;
//# sourceMappingURL=sentryAppComponentsStore.jsx.map