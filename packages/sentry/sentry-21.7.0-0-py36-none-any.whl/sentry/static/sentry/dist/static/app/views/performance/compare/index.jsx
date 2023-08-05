Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var content_1 = tslib_1.__importDefault(require("./content"));
var fetchEvent_1 = tslib_1.__importDefault(require("./fetchEvent"));
var TransactionComparisonPage = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionComparisonPage, _super);
    function TransactionComparisonPage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionComparisonPage.prototype.getEventSlugs = function () {
        var _a = this.props.params, baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        var validatedBaselineEventSlug = typeof baselineEventSlug === 'string' ? baselineEventSlug.trim() : undefined;
        var validatedRegressionEventSlug = typeof regressionEventSlug === 'string' ? regressionEventSlug.trim() : undefined;
        return {
            baselineEventSlug: validatedBaselineEventSlug,
            regressionEventSlug: validatedRegressionEventSlug,
        };
    };
    TransactionComparisonPage.prototype.fetchEvent = function (eventSlug, renderFunc) {
        if (!eventSlug) {
            return <notFound_1.default />;
        }
        var organization = this.props.organization;
        return (<fetchEvent_1.default orgSlug={organization.slug} eventSlug={eventSlug}>
        {renderFunc}
      </fetchEvent_1.default>);
    };
    TransactionComparisonPage.prototype.renderComparison = function (_a) {
        var _this = this;
        var baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        return this.fetchEvent(baselineEventSlug, function (baselineEventResults) {
            return _this.fetchEvent(regressionEventSlug, function (regressionEventResults) {
                if (baselineEventResults.isLoading || regressionEventResults.isLoading) {
                    return <loadingIndicator_1.default />;
                }
                if (baselineEventResults.error || regressionEventResults.error) {
                    if (baselineEventResults.error) {
                        Sentry.captureException(baselineEventResults.error);
                    }
                    if (regressionEventResults.error) {
                        Sentry.captureException(regressionEventResults.error);
                    }
                    return <loadingError_1.default />;
                }
                if (!baselineEventResults.event || !regressionEventResults.event) {
                    return <notFound_1.default />;
                }
                var _a = _this.props, organization = _a.organization, location = _a.location, params = _a.params;
                return (<content_1.default organization={organization} location={location} params={params} baselineEvent={baselineEventResults.event} regressionEvent={regressionEventResults.event}/>);
            });
        });
    };
    TransactionComparisonPage.prototype.getDocumentTitle = function (_a) {
        var baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        if (typeof baselineEventSlug === 'string' &&
            typeof regressionEventSlug === 'string') {
            var title = locale_1.t('Comparing %s to %s', baselineEventSlug, regressionEventSlug);
            return [title, locale_1.t('Performance')].join(' - ');
        }
        return [locale_1.t('Transaction Comparison'), locale_1.t('Performance')].join(' - ');
    };
    TransactionComparisonPage.prototype.render = function () {
        var organization = this.props.organization;
        var _a = this.getEventSlugs(), baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle({ baselineEventSlug: baselineEventSlug, regressionEventSlug: regressionEventSlug })} orgSlug={organization.slug}>
        <React.Fragment>
          <StyledPageContent>
            <lightWeightNoProjectMessage_1.default organization={organization}>
              {this.renderComparison({ baselineEventSlug: baselineEventSlug, regressionEventSlug: regressionEventSlug })}
            </lightWeightNoProjectMessage_1.default>
          </StyledPageContent>
        </React.Fragment>
      </sentryDocumentTitle_1.default>);
    };
    return TransactionComparisonPage;
}(React.PureComponent));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
exports.default = withOrganization_1.default(TransactionComparisonPage);
var templateObject_1;
//# sourceMappingURL=index.jsx.map