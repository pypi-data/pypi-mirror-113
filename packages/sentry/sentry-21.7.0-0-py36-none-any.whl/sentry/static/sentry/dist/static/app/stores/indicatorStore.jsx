Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var indicatorActions_1 = tslib_1.__importDefault(require("app/actions/indicatorActions"));
var locale_1 = require("app/locale");
var storeConfig = {
    items: [],
    lastId: 0,
    init: function () {
        this.items = [];
        this.lastId = 0;
        this.listenTo(indicatorActions_1.default.append, this.append);
        this.listenTo(indicatorActions_1.default.replace, this.add);
        this.listenTo(indicatorActions_1.default.remove, this.remove);
        this.listenTo(indicatorActions_1.default.clear, this.clear);
    },
    get: function () {
        return this.items;
    },
    addSuccess: function (message) {
        return this.add(message, 'success', { duration: 2000 });
    },
    addError: function (message) {
        if (message === void 0) { message = locale_1.t('An error occurred'); }
        return this.add(message, 'error', { duration: 2000 });
    },
    addMessage: function (message, type, _a) {
        var _this = this;
        if (_a === void 0) { _a = {}; }
        var append = _a.append, options = tslib_1.__rest(_a, ["append"]);
        var indicator = {
            id: this.lastId++,
            message: message,
            type: type,
            options: options,
            clearId: null,
        };
        if (options.duration) {
            indicator.clearId = window.setTimeout(function () {
                _this.remove(indicator);
            }, options.duration);
        }
        var newItems = append ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.items)), [indicator]) : [indicator];
        this.items = newItems;
        this.trigger(this.items);
        return indicator;
    },
    append: function (message, type, options) {
        return this.addMessage(message, type, tslib_1.__assign(tslib_1.__assign({}, options), { append: true }));
    },
    add: function (message, type, options) {
        if (type === void 0) { type = 'loading'; }
        if (options === void 0) { options = {}; }
        return this.addMessage(message, type, tslib_1.__assign(tslib_1.__assign({}, options), { append: false }));
    },
    clear: function () {
        this.items = [];
        this.trigger(this.items);
    },
    remove: function (indicator) {
        if (!indicator) {
            return;
        }
        this.items = this.items.filter(function (item) { return item !== indicator; });
        if (indicator.clearId) {
            window.clearTimeout(indicator.clearId);
            indicator.clearId = null;
        }
        this.trigger(this.items);
    },
};
var IndicatorStore = reflux_1.default.createStore(storeConfig);
exports.default = IndicatorStore;
//# sourceMappingURL=indicatorStore.jsx.map