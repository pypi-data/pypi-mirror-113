Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
// This is react-router v4 <Redirect to="path/" /> component to allow things
// to be declarative.
var Redirect = /** @class */ (function (_super) {
    tslib_1.__extends(Redirect, _super);
    function Redirect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Redirect.prototype.componentDidMount = function () {
        this.props.router.replace(this.props.to);
    };
    Redirect.prototype.render = function () {
        return null;
    };
    return Redirect;
}(react_1.Component));
exports.default = Redirect;
//# sourceMappingURL=redirect.jsx.map