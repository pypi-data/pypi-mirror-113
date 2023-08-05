Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var organizationsActions_1 = tslib_1.__importDefault(require("app/actions/organizationsActions"));
var organizationsStoreConfig = {
    listenables: [organizationsActions_1.default],
    state: [],
    loaded: false,
    // So we can use Reflux.connect in a component mixin
    getInitialState: function () {
        return this.state;
    },
    init: function () {
        this.state = [];
        this.loaded = false;
    },
    onUpdate: function (org) {
        this.add(org);
    },
    onChangeSlug: function (prev, next) {
        if (prev.slug === next.slug) {
            return;
        }
        this.remove(prev.slug);
        this.add(next);
    },
    onRemoveSuccess: function (slug) {
        this.remove(slug);
    },
    get: function (slug) {
        return this.state.find(function (item) { return item.slug === slug; });
    },
    getAll: function () {
        return this.state;
    },
    remove: function (slug) {
        this.state = this.state.filter(function (item) { return slug !== item.slug; });
        this.trigger(this.state);
    },
    add: function (item) {
        var _this = this;
        var match = false;
        this.state.forEach(function (existing, idx) {
            if (existing.id === item.id) {
                item = tslib_1.__assign(tslib_1.__assign({}, existing), item);
                _this.state[idx] = item;
                match = true;
            }
        });
        if (!match) {
            this.state = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.state)), [item]);
        }
        this.trigger(this.state);
    },
    load: function (items) {
        this.state = items;
        this.loaded = true;
        this.trigger(items);
    },
};
var OrganizationsStore = reflux_1.default.createStore(organizationsStoreConfig);
exports.default = OrganizationsStore;
//# sourceMappingURL=organizationsStore.jsx.map