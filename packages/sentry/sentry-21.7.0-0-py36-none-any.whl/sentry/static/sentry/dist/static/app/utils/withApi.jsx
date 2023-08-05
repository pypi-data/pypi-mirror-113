Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var api_1 = require("app/api");
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * React Higher-Order Component (HoC) that provides "api" client when mounted,
 * and clears API requests when component is unmounted.
 */
var withApi = function (WrappedComponent, _a) {
    var _b;
    var _c = _a === void 0 ? {} : _a, persistInFlight = _c.persistInFlight;
    return _b = /** @class */ (function (_super) {
            tslib_1.__extends(class_1, _super);
            function class_1(props) {
                var _this = _super.call(this, props) || this;
                _this.api = new api_1.Client();
                return _this;
            }
            class_1.prototype.componentWillUnmount = function () {
                if (!persistInFlight) {
                    this.api.clear();
                }
            };
            class_1.prototype.render = function () {
                var _a = this.props, api = _a.api, props = tslib_1.__rest(_a, ["api"]);
                return <WrappedComponent {...tslib_1.__assign({ api: api !== null && api !== void 0 ? api : this.api }, props)}/>;
            };
            return class_1;
        }(React.Component)),
        _b.displayName = "withApi(" + getDisplayName_1.default(WrappedComponent) + ")",
        _b;
};
exports.default = withApi;
//# sourceMappingURL=withApi.jsx.map