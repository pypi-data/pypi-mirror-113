Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var callIfFunction_1 = require("app/utils/callIfFunction");
var ScrollToTop = /** @class */ (function (_super) {
    tslib_1.__extends(ScrollToTop, _super);
    function ScrollToTop() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ScrollToTop.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, disable = _a.disable, location = _a.location;
        var shouldDisable = callIfFunction_1.callIfFunction(disable, location, prevProps.location);
        if (!shouldDisable && this.props.location !== prevProps.location) {
            window.scrollTo(0, 0);
        }
    };
    ScrollToTop.prototype.render = function () {
        return this.props.children;
    };
    return ScrollToTop;
}(react_1.Component));
exports.default = ScrollToTop;
//# sourceMappingURL=scrollToTop.jsx.map