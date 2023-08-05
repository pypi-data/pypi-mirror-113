Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var sentryAppComponentsStore_1 = tslib_1.__importDefault(require("app/stores/sentryAppComponentsStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
function withSentryAppComponents(WrappedComponent, _a) {
    var _b = _a === void 0 ? {} : _a, componentType = _b.componentType;
    var WithSentryAppComponents = /** @class */ (function (_super) {
        tslib_1.__extends(WithSentryAppComponents, _super);
        function WithSentryAppComponents() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { components: sentryAppComponentsStore_1.default.getAll() };
            _this.unsubscribe = sentryAppComponentsStore_1.default.listen(function () { return _this.setState({ components: sentryAppComponentsStore_1.default.getAll() }); }, undefined);
            return _this;
        }
        WithSentryAppComponents.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithSentryAppComponents.prototype.render = function () {
            var _a = this.props, components = _a.components, props = tslib_1.__rest(_a, ["components"]);
            return (<WrappedComponent {...tslib_1.__assign({ components: components !== null && components !== void 0 ? components : sentryAppComponentsStore_1.default.getComponentByType(componentType) }, props)}/>);
        };
        WithSentryAppComponents.displayName = "withSentryAppComponents(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithSentryAppComponents;
    }(React.Component));
    return WithSentryAppComponents;
}
exports.default = withSentryAppComponents;
//# sourceMappingURL=withSentryAppComponents.jsx.map