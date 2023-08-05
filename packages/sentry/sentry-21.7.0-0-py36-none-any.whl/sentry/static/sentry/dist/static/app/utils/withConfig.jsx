Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Higher order component that passes the config object to the wrapped component
 */
function withConfig(WrappedComponent) {
    var WithConfig = /** @class */ (function (_super) {
        tslib_1.__extends(WithConfig, _super);
        function WithConfig() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { config: configStore_1.default.getConfig() };
            _this.unsubscribe = configStore_1.default.listen(function () { return _this.setState({ config: configStore_1.default.getConfig() }); }, undefined);
            return _this;
        }
        WithConfig.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithConfig.prototype.render = function () {
            var _a = this.props, config = _a.config, props = tslib_1.__rest(_a, ["config"]);
            return (<WrappedComponent {...tslib_1.__assign({ config: config !== null && config !== void 0 ? config : this.state.config }, props)}/>);
        };
        WithConfig.displayName = "withConfig(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithConfig;
    }(React.Component));
    return WithConfig;
}
exports.default = withConfig;
//# sourceMappingURL=withConfig.jsx.map