Object.defineProperty(exports, "__esModule", { value: true });
exports.Indicators = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var indicator_1 = require("app/actionCreators/indicator");
var toastIndicator_1 = tslib_1.__importDefault(require("app/components/alerts/toastIndicator"));
var indicatorStore_1 = tslib_1.__importDefault(require("app/stores/indicatorStore"));
var theme_1 = require("app/utils/theme");
var Toasts = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: fixed;\n  right: 30px;\n  bottom: 30px;\n  z-index: ", ";\n"], ["\n  position: fixed;\n  right: 30px;\n  bottom: 30px;\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.toast; });
var Indicators = /** @class */ (function (_super) {
    tslib_1.__extends(Indicators, _super);
    function Indicators() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDismiss = function (indicator) {
            indicator_1.removeIndicator(indicator);
        };
        return _this;
    }
    Indicators.prototype.render = function () {
        var _this = this;
        var _a = this.props, items = _a.items, props = tslib_1.__rest(_a, ["items"]);
        return (<Toasts {...props}>
        <framer_motion_1.AnimatePresence>
          {items.map(function (indicator, i) { return (
            // We purposefully use `i` as key here because of transitions
            // Toasts can now queue up, so when we change from [firstToast] -> [secondToast],
            // we don't want to  animate `firstToast` out and `secondToast` in, rather we want
            // to replace `firstToast` with `secondToast`
            <toastIndicator_1.default onDismiss={_this.handleDismiss} indicator={indicator} key={i}/>); })}
        </framer_motion_1.AnimatePresence>
      </Toasts>);
    };
    Indicators.defaultProps = {
        items: [],
    };
    return Indicators;
}(react_1.Component));
exports.Indicators = Indicators;
var IndicatorsContainer = /** @class */ (function (_super) {
    tslib_1.__extends(IndicatorsContainer, _super);
    function IndicatorsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { items: indicatorStore_1.default.get() };
        _this.unlistener = indicatorStore_1.default.listen(function (items) {
            _this.setState({ items: items });
        }, undefined);
        return _this;
    }
    IndicatorsContainer.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    IndicatorsContainer.prototype.render = function () {
        // #NEW-SETTINGS - remove ThemeProvider here once new settings is merged
        // `alerts.html` django view includes this container and doesn't have a theme provider
        // not even sure it is used in django views but this is just an easier temp solution
        return (<react_2.ThemeProvider theme={theme_1.lightTheme}>
        <Indicators {...this.props} items={this.state.items}/>
      </react_2.ThemeProvider>);
    };
    return IndicatorsContainer;
}(react_1.Component));
exports.default = IndicatorsContainer;
var templateObject_1;
//# sourceMappingURL=indicators.jsx.map