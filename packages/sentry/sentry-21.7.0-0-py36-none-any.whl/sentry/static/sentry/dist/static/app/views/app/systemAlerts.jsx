Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var alertStore_1 = tslib_1.__importDefault(require("app/stores/alertStore"));
var theme_1 = require("app/utils/theme");
var alertMessage_1 = tslib_1.__importDefault(require("./alertMessage"));
var SystemAlerts = /** @class */ (function (_super) {
    tslib_1.__extends(SystemAlerts, _super);
    function SystemAlerts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.unlistener = alertStore_1.default.listen(function (alerts) { return _this.setState({ alerts: alerts }); }, undefined);
        return _this;
    }
    SystemAlerts.prototype.getInitialState = function () {
        return {
            alerts: alertStore_1.default.getInitialState(),
        };
    };
    SystemAlerts.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    SystemAlerts.prototype.render = function () {
        var className = this.props.className;
        var alerts = this.state.alerts;
        return (<react_1.ThemeProvider theme={theme_1.lightTheme}>
        <div className={className}>
          {alerts.map(function (alert, index) { return (<alertMessage_1.default alert={alert} key={alert.id + "-" + index} system/>); })}
        </div>
      </react_1.ThemeProvider>);
    };
    return SystemAlerts;
}(React.Component));
exports.default = SystemAlerts;
//# sourceMappingURL=systemAlerts.jsx.map