Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var routeError_1 = tslib_1.__importDefault(require("app/views/routeError"));
function errorHandler(Component) {
    var ErrorHandler = /** @class */ (function (_super) {
        tslib_1.__extends(ErrorHandler, _super);
        function ErrorHandler() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                // we are explicit if an error has been thrown since errors thrown are not guaranteed
                // to be truthy (e.g. throw null).
                hasError: false,
                error: undefined,
            };
            return _this;
        }
        ErrorHandler.getDerivedStateFromError = function (error) {
            // Update state so the next render will show the fallback UI.
            return {
                hasError: true,
                error: error,
            };
        };
        ErrorHandler.prototype.componentDidCatch = function (_error, info) {
            // eslint-disable-next-line no-console
            console.error('Component stack trace caught in <ErrorHandler />:', info.componentStack);
        };
        ErrorHandler.prototype.render = function () {
            if (this.state.hasError) {
                return <routeError_1.default error={this.state.error}/>;
            }
            return <Component {...this.props}/>;
        };
        return ErrorHandler;
    }(React.Component));
    return ErrorHandler;
}
exports.default = errorHandler;
//# sourceMappingURL=errorHandler.jsx.map