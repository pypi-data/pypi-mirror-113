Object.defineProperty(exports, "__esModule", { value: true });
exports.RouteError = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
var RouteError = /** @class */ (function (_super) {
    tslib_1.__extends(RouteError, _super);
    function RouteError() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RouteError.prototype.UNSAFE_componentWillMount = function () {
        var error = this.props.error;
        var _a = this.props, disableLogSentry = _a.disableLogSentry, disableReport = _a.disableReport, organization = _a.organization, project = _a.project, routes = _a.routes;
        if (disableLogSentry) {
            return;
        }
        if (!error) {
            return;
        }
        var route = getRouteStringFromRoutes_1.default(routes);
        var enrichScopeContext = function (scope) {
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            return scope;
        };
        if (route) {
            /**
             * Unexpectedly, error.message would sometimes not have a setter property, causing another exception to be thrown,
             * and losing the original error in the process. Wrapping the mutation in a try-catch in an attempt to preserve
             * the original error for logging.
             * See https://github.com/getsentry/sentry/issues/16314 for more details.
             */
            try {
                error.message = error.message + ": " + route;
            }
            catch (e) {
                Sentry.withScope(function (scope) {
                    enrichScopeContext(scope);
                    Sentry.captureException(e);
                });
            }
        }
        // TODO(dcramer): show something in addition to embed (that contains it?)
        // throw this in a timeout so if it errors we dont fall over
        this._timeout = window.setTimeout(function () {
            Sentry.withScope(function (scope) {
                enrichScopeContext(scope);
                Sentry.captureException(error);
            });
            if (!disableReport) {
                Sentry.showReportDialog();
            }
        });
    };
    RouteError.prototype.componentWillUnmount = function () {
        var _a;
        if (this._timeout) {
            window.clearTimeout(this._timeout);
        }
        (_a = document.querySelector('.sentry-error-embed-wrapper')) === null || _a === void 0 ? void 0 : _a.remove();
    };
    RouteError.prototype.render = function () {
        // TODO(dcramer): show additional resource links
        return (<alert_1.default icon={<icons_1.IconWarning size="md"/>} type="error">
        <Heading>
          <span>{locale_1.t('Oops! Something went wrong')}</span>
        </Heading>
        <p>
          {locale_1.t("\n          It looks like you've hit an issue in our client application. Don't worry though!\n          We use Sentry to monitor Sentry and it's likely we're already looking into this!\n          ")}
        </p>
        <p>{locale_1.t("If you're daring, you may want to try the following:")}</p>
        <ul>
          {window && window.adblockSuspected && (<li>
              {locale_1.t("We detected something AdBlock-like. Try disabling it, as it's known to cause issues.")}
            </li>)}
          <li>
            {locale_1.tct("Give it a few seconds and [link:reload the page].", {
                link: (<a onClick={function () {
                        window.location.href = window.location.href;
                    }}/>),
            })}
          </li>
          <li>
            {locale_1.tct("If all else fails, [link:contact us] with more details.", {
                link: <a href="https://github.com/getsentry/sentry/issues/new/choose"/>,
            })}
          </li>
        </ul>
      </alert_1.default>);
    };
    return RouteError;
}(react_1.Component));
exports.RouteError = RouteError;
var Heading = styled_1.default('h3')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  font-weight: normal;\n\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  font-weight: normal;\n\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, space_1.default(1.5));
exports.default = react_router_1.withRouter(withOrganization_1.default(withProject_1.default(RouteError)));
var templateObject_1;
//# sourceMappingURL=routeError.jsx.map