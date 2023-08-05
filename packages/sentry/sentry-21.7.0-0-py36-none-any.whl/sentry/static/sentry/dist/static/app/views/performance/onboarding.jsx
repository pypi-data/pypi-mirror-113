Object.defineProperty(exports, "__esModule", { value: true });
exports.PERFORMANCE_TOUR_STEPS = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var performance_empty_state_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-empty-state.svg"));
var performance_tour_alert_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-alert.svg"));
var performance_tour_correlate_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-correlate.svg"));
var performance_tour_metrics_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-metrics.svg"));
var performance_tour_trace_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-trace.svg"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureTourModal_1 = tslib_1.__importStar(require("app/components/modals/featureTourModal"));
var onboardingPanel_1 = tslib_1.__importDefault(require("app/components/onboardingPanel"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var performanceSetupUrl = 'https://docs.sentry.io/performance-monitoring/getting-started/';
var docsLink = (<button_1.default external href={performanceSetupUrl}>
    {locale_1.t('Setup')}
  </button_1.default>);
exports.PERFORMANCE_TOUR_STEPS = [
    {
        title: locale_1.t('Track Application Metrics'),
        image: <featureTourModal_1.TourImage src={performance_tour_metrics_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Monitor your slowest pageloads and APIs to see which users are having the worst time.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Correlate Errors and Performance'),
        image: <featureTourModal_1.TourImage src={performance_tour_correlate_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('See what errors occurred within a transaction and the impact of those errors.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Watch and Alert'),
        image: <featureTourModal_1.TourImage src={performance_tour_alert_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Highlight mission-critical pages and APIs and set latency alerts to notify you before things go wrong.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Trace Across Systems'),
        image: <featureTourModal_1.TourImage src={performance_tour_trace_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t("Follow a trace from a user's session and drill down to identify any bottlenecks that occur.")}
      </featureTourModal_1.TourText>),
    },
];
function Onboarding(_a) {
    var organization = _a.organization;
    function handleAdvance(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.tour.advance',
            eventName: 'Performance Views: Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    function handleClose(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.tour.close',
            eventName: 'Performance Views: Tour Close',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    return (<onboardingPanel_1.default image={<PerfImage src={performance_empty_state_svg_1.default}/>}>
      <h3>{locale_1.t('Pinpoint problems')}</h3>
      <p>
        {locale_1.t('Something seem slow? Track down transactions to connect the dots between 10-second page loads and poor-performing API calls or slow database queries.')}
      </p>
      <ButtonList gap={1}>
        <featureTourModal_1.default steps={exports.PERFORMANCE_TOUR_STEPS} onAdvance={handleAdvance} onCloseModal={handleClose} doneUrl={performanceSetupUrl} doneText={locale_1.t('Start Setup')}>
          {function (_a) {
            var showModal = _a.showModal;
            return (<button_1.default priority="default" onClick={function () {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'performance_views.tour.start',
                        eventName: 'Performance Views: Tour Start',
                        organization_id: parseInt(organization.id, 10),
                    });
                    showModal();
                }}>
              {locale_1.t('Take a Tour')}
            </button_1.default>);
        }}
        </featureTourModal_1.default>
        <button_1.default priority="primary" target="_blank" href="https://docs.sentry.io/performance-monitoring/getting-started/">
          {locale_1.t('Start Setup')}
        </button_1.default>
      </ButtonList>
    </onboardingPanel_1.default>);
}
var PerfImage = styled_1.default('img')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 50px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 50px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var ButtonList = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
exports.default = Onboarding;
var templateObject_1, templateObject_2;
//# sourceMappingURL=onboarding.jsx.map