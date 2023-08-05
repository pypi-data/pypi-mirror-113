Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var alertActions_1 = tslib_1.__importDefault(require("app/actions/alertActions"));
var utils_1 = require("app/utils");
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var storeConfig = {
    listenables: alertActions_1.default,
    alerts: [],
    count: 0,
    init: function () {
        this.alerts = [];
        this.count = 0;
    },
    getInitialState: function () {
        return this.alerts;
    },
    onAddAlert: function (alert) {
        var _this = this;
        var alertAlreadyExists = this.alerts.some(function (a) { return a.id === alert.id; });
        if (alertAlreadyExists && alert.noDuplicates) {
            return;
        }
        if (utils_1.defined(alert.id)) {
            var mutedData = localStorage_1.default.getItem('alerts:muted');
            if (typeof mutedData === 'string' && mutedData.length) {
                var expirations = JSON.parse(mutedData);
                // Remove any objects that have passed their mute duration.
                var now = Math.floor(new Date().valueOf() / 1000);
                for (var key in expirations) {
                    if (expirations.hasOwnProperty(key) && expirations[key] < now) {
                        delete expirations[key];
                    }
                }
                localStorage_1.default.setItem('alerts:muted', JSON.stringify(expirations));
                if (expirations.hasOwnProperty(alert.id)) {
                    return;
                }
            }
        }
        else {
            if (!utils_1.defined(alert.expireAfter)) {
                alert.expireAfter = 5000;
            }
        }
        if (alert.expireAfter && !alert.neverExpire) {
            window.setTimeout(function () {
                _this.onCloseAlert(alert);
            }, alert.expireAfter);
        }
        alert.key = this.count++;
        // intentionally recreate array via concat because of Reflux
        // "bug" where React components are given same reference to tracked
        // data objects, and don't *see* that values have changed
        this.alerts = this.alerts.concat([alert]);
        this.trigger(this.alerts);
    },
    onCloseAlert: function (alert, duration) {
        if (duration === void 0) { duration = 60 * 60 * 7 * 24; }
        if (utils_1.defined(alert.id) && utils_1.defined(duration)) {
            var expiry = Math.floor(new Date().valueOf() / 1000) + duration;
            var mutedData = localStorage_1.default.getItem('alerts:muted');
            var expirations = {};
            if (typeof mutedData === 'string' && expirations.length) {
                expirations = JSON.parse(mutedData);
            }
            expirations[alert.id] = expiry;
            localStorage_1.default.setItem('alerts:muted', JSON.stringify(expirations));
        }
        // TODO(dcramer): we need some animations here for closing alerts
        this.alerts = this.alerts.filter(function (item) { return alert !== item; });
        this.trigger(this.alerts);
    },
};
var AlertStore = reflux_1.default.createStore(storeConfig);
exports.default = AlertStore;
//# sourceMappingURL=alertStore.jsx.map