Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var congrats_robots_placeholder_jpg_1 = tslib_1.__importDefault(require("sentry-images/spot/congrats-robots-placeholder.jpg"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Placeholder = function () { return (<PlaceholderImage alt={locale_1.t('Congrats, you have no unresolved issues')} src={congrats_robots_placeholder_jpg_1.default}/>); };
var Message = function () { return (<React.Fragment>
    <EmptyMessage>
      {locale_1.t("We couldn't find any issues that matched your filters.")}
    </EmptyMessage>
    <p>{locale_1.t('Get out there and write some broken code!')}</p>
  </React.Fragment>); };
var CongratsRobotsVideo = React.lazy(function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('./congratsRobots')); }); });
/**
 * Error boundary for loading the robots video.
 * This can error because of the file size of the video
 *
 * Silently ignore the error, this isn't really important enough to
 * capture in Sentry
 */
var ErrorBoundary = /** @class */ (function (_super) {
    tslib_1.__extends(ErrorBoundary, _super);
    function ErrorBoundary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasError: false,
        };
        return _this;
    }
    ErrorBoundary.getDerivedStateFromError = function () {
        return {
            hasError: true,
        };
    };
    ErrorBoundary.prototype.render = function () {
        if (this.state.hasError) {
            return <Placeholder />;
        }
        return this.props.children;
    };
    return ErrorBoundary;
}(React.Component));
var NoUnresolvedIssues = function () { return (<Wrapper>
    <ErrorBoundary>
      <React.Suspense fallback={<Placeholder />}>
        <CongratsRobotsVideo />
      </React.Suspense>
    </ErrorBoundary>
    <Message />
  </Wrapper>); };
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  color: ", ";\n\n  @media (max-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  display: flex;\n  padding: ", " ", ";\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  color: ", ";\n\n  @media (max-width: ", ") {\n    font-size: ", ";\n  }\n"])), space_1.default(4), space_1.default(4), function (p) { return p.theme.subText; }, function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.fontSizeMedium; });
var EmptyMessage = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 600;\n\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  font-weight: 600;\n\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.fontSizeExtraLarge; });
var PlaceholderImage = styled_1.default('img')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  max-height: 320px; /* This should be same height as video in CongratsRobots */\n"], ["\n  max-height: 320px; /* This should be same height as video in CongratsRobots */\n"])));
exports.default = NoUnresolvedIssues;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=noUnresolvedIssues.jsx.map