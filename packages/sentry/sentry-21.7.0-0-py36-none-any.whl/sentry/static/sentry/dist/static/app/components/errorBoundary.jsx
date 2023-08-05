Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var detailedError_1 = tslib_1.__importDefault(require("app/components/errors/detailedError"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var exclamation = ['Raspberries', 'Snap', 'Frig', 'Welp', 'Uhhhh', 'Hmmm'];
function getExclamation() {
    return exclamation[Math.floor(Math.random() * exclamation.length)];
}
var ErrorBoundary = /** @class */ (function (_super) {
    tslib_1.__extends(ErrorBoundary, _super);
    function ErrorBoundary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: null,
        };
        _this._isMounted = false;
        return _this;
    }
    ErrorBoundary.prototype.componentDidMount = function () {
        var _this = this;
        this._isMounted = true;
        // Listen for route changes so we can clear error
        this.unlistenBrowserHistory = react_router_1.browserHistory.listen(function () {
            // Prevent race between component unmount and browserHistory change
            // Setting state on a component that is being unmounted throws an error
            if (_this._isMounted) {
                _this.setState({ error: null });
            }
        });
    };
    ErrorBoundary.prototype.componentDidCatch = function (error, errorInfo) {
        var errorTag = this.props.errorTag;
        this.setState({ error: error });
        Sentry.withScope(function (scope) {
            if (errorTag) {
                Object.keys(errorTag).forEach(function (tag) { return scope.setTag(tag, errorTag[tag]); });
            }
            scope.setExtra('errorInfo', errorInfo);
            Sentry.captureException(error);
        });
    };
    ErrorBoundary.prototype.componentWillUnmount = function () {
        this._isMounted = false;
        if (this.unlistenBrowserHistory) {
            this.unlistenBrowserHistory();
        }
    };
    ErrorBoundary.prototype.render = function () {
        var error = this.state.error;
        if (!error) {
            // when there's not an error, render children untouched
            return this.props.children;
        }
        var _a = this.props, customComponent = _a.customComponent, mini = _a.mini, message = _a.message, className = _a.className;
        if (typeof customComponent !== 'undefined') {
            return customComponent;
        }
        if (mini) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>} className={className}>
          {message || locale_1.t('There was a problem rendering this component')}
        </alert_1.default>);
        }
        return (<Wrapper>
        <detailedError_1.default heading={getDynamicText_1.default({
                value: getExclamation(),
                fixed: exclamation[0],
            })} message={locale_1.t("Something went horribly wrong rendering this page.\nWe use a decent error reporting service so this will probably be fixed soon. Unless our error reporting service is also broken. That would be awkward.\nAnyway, we apologize for the inconvenience.")}/>
        <StackTrace>{error.toString()}</StackTrace>
      </Wrapper>);
    };
    ErrorBoundary.defaultProps = {
        mini: false,
    };
    return ErrorBoundary;
}(React.Component));
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding: ", "px;\n  max-width: 1000px;\n  margin: auto;\n"], ["\n  color: ", ";\n  padding: ", "px;\n  max-width: 1000px;\n  margin: auto;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.grid * 3; });
var StackTrace = styled_1.default('pre')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  white-space: pre-wrap;\n  margin: 32px;\n  margin-left: 85px;\n  margin-right: 18px;\n"], ["\n  white-space: pre-wrap;\n  margin: 32px;\n  margin-left: 85px;\n  margin-right: 18px;\n"])));
exports.default = ErrorBoundary;
var templateObject_1, templateObject_2;
//# sourceMappingURL=errorBoundary.jsx.map