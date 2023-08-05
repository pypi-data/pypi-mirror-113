Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var ExternalIssueStore = reflux_1.default.createStore({
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
    get: function (id) {
        return this.items.find(function (item) { return item.id === id; });
    },
    getAll: function () {
        return this.items;
    },
    add: function (issue) {
        if (!this.items.some(function (i) { return i.id === issue.id; })) {
            this.items = this.items.concat([issue]);
            this.trigger(this.items);
        }
    },
});
exports.default = ExternalIssueStore;
//# sourceMappingURL=externalIssueStore.jsx.map