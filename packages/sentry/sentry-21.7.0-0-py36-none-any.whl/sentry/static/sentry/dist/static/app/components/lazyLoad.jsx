Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var retryableImport_1 = tslib_1.__importDefault(require("app/utils/retryableImport"));
var LazyLoad = /** @class */ (function (_super) {
    tslib_1.__extends(LazyLoad, _super);
    function LazyLoad() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            Component: null,
            error: null,
        };
        _this.handleFetchError = function (error) {
            Sentry.withScope(function (scope) {
                if (utils_1.isWebpackChunkLoadingError(error)) {
                    scope.setFingerprint(['webpack', 'error loading chunk']);
                }
                Sentry.captureException(error);
            });
            _this.handleError(error);
        };
        _this.handleError = function (error) {
            // eslint-disable-next-line no-console
            console.error(error);
            _this.setState({ error: error });
        };
        _this.fetchComponent = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var getComponent, _a, err_1;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        getComponent = this.componentGetter;
                        if (getComponent === undefined) {
                            return [2 /*return*/];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, retryableImport_1.default(getComponent)];
                    case 2:
                        _a.apply(this, [(_b.Component = _c.sent(), _b)]);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        this.handleFetchError(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.fetchRetry = function () {
            _this.setState({ error: null }, _this.fetchComponent);
        };
        return _this;
    }
    LazyLoad.prototype.componentDidMount = function () {
        this.fetchComponent();
    };
    LazyLoad.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // No need to refetch when component does not change
        if (nextProps.component && nextProps.component === this.props.component) {
            return;
        }
        // This is to handle the following case:
        // <Route path="a/">
        //   <Route path="b/" component={LazyLoad} componentPromise={...} />
        //   <Route path="c/" component={LazyLoad} componentPromise={...} />
        // </Route>
        //
        // `LazyLoad` will get not fully remount when we switch between `b` and `c`,
        // instead will just re-render.  Refetch if route paths are different
        if (nextProps.route && nextProps.route === this.props.route) {
            return;
        }
        // If `this.fetchComponent` is not in callback,
        // then there's no guarantee that new Component will be rendered
        this.setState({
            Component: null,
        }, this.fetchComponent);
    };
    LazyLoad.prototype.componentDidCatch = function (error) {
        Sentry.captureException(error);
        this.handleError(error);
    };
    Object.defineProperty(LazyLoad.prototype, "componentGetter", {
        get: function () {
            var _a, _b;
            return (_a = this.props.component) !== null && _a !== void 0 ? _a : (_b = this.props.route) === null || _b === void 0 ? void 0 : _b.componentPromise;
        },
        enumerable: false,
        configurable: true
    });
    LazyLoad.prototype.render = function () {
        var _a = this.state, Component = _a.Component, error = _a.error;
        var _b = this.props, hideBusy = _b.hideBusy, hideError = _b.hideError, _component = _b.component, otherProps = tslib_1.__rest(_b, ["hideBusy", "hideError", "component"]);
        if (error && !hideError) {
            return (<LoadingErrorContainer>
          <loadingError_1.default onRetry={this.fetchRetry} message={locale_1.t('There was an error loading a component.')}/>
        </LoadingErrorContainer>);
        }
        if (!Component && !hideBusy) {
            return (<LoadingContainer>
          <loadingIndicator_1.default />
        </LoadingContainer>);
        }
        if (Component === null) {
            return null;
        }
        return <Component {...otherProps}/>;
    };
    return LazyLoad;
}(React.Component));
var LoadingContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var LoadingErrorContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
exports.default = LazyLoad;
var templateObject_1, templateObject_2;
//# sourceMappingURL=lazyLoad.jsx.map