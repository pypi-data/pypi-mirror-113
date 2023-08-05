Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var extend_1 = tslib_1.__importDefault(require("lodash/extend"));
var isArray_1 = tslib_1.__importDefault(require("lodash/isArray"));
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var storeConfig = {
    items: [],
    itemsById: {},
    init: function () {
        this.reset();
    },
    reset: function () {
        this.items = [];
    },
    loadInitialData: function (items) {
        var _this = this;
        this.reset();
        var itemIds = new Set();
        items.forEach(function (item) {
            itemIds.add(item.id);
            _this.items.push(item);
        });
        this.trigger(itemIds);
    },
    add: function (items) {
        var _this = this;
        if (!isArray_1.default(items)) {
            items = [items];
        }
        var itemsById = {};
        var itemIds = new Set();
        items.forEach(function (item) {
            itemsById[item.id] = item;
            itemIds.add(item.id);
        });
        items.forEach(function (item, idx) {
            if (itemsById[item.id]) {
                _this.items[idx] = extend_1.default(true, {}, item, itemsById[item.id]);
                delete itemsById[item.id];
            }
        });
        for (var itemId in itemsById) {
            this.items.push(itemsById[itemId]);
        }
        this.trigger(itemIds);
    },
    remove: function (itemId) {
        var _this = this;
        this.items.forEach(function (item, idx) {
            if (item.id === itemId) {
                _this.items.splice(idx, idx + 1);
            }
        });
        this.trigger(new Set([itemId]));
    },
    get: function (id) {
        for (var i = 0; i < this.items.length; i++) {
            if (this.items[i].id === id) {
                return this.items[i];
            }
        }
        return undefined;
    },
    getAllItemIds: function () {
        return this.items.map(function (item) { return item.id; });
    },
    getAllItems: function () {
        return this.items;
    },
};
var EventStore = reflux_1.default.createStore(storeConfig);
exports.default = EventStore;
//# sourceMappingURL=eventStore.jsx.map