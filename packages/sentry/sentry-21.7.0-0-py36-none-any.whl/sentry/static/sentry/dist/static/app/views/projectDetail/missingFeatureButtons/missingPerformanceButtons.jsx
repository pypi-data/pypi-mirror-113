Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureTourModal_1 = tslib_1.__importDefault(require("app/components/modals/featureTourModal"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var onboarding_1 = require("app/views/performance/onboarding");
var DOCS_URL = 'https://docs.sentry.io/performance-monitoring/getting-started/';
function MissingPerformanceButtons(_a) {
    var organization = _a.organization;
    function handleTourAdvance(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'project_detail.performance_tour.advance',
            eventName: 'Project Detail: Performance Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    function handleClose(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'project_detail.performance_tour.close',
            eventName: 'Project Detail: Performance Tour Close',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    return (<feature_1.default hookName="feature-disabled:project-performance-score-card" features={['performance-view']} organization={organization}>
      <StyledButtonBar gap={1}>
        <button_1.default size="small" priority="primary" external href={DOCS_URL}>
          {locale_1.t('Start Setup')}
        </button_1.default>

        <featureTourModal_1.default steps={onboarding_1.PERFORMANCE_TOUR_STEPS} onAdvance={handleTourAdvance} onCloseModal={handleClose} doneText={locale_1.t('Start Setup')} doneUrl={DOCS_URL}>
          {function (_a) {
            var showModal = _a.showModal;
            return (<button_1.default size="small" onClick={showModal}>
              {locale_1.t('Get a tour')}
            </button_1.default>);
        }}
        </featureTourModal_1.default>
      </StyledButtonBar>
    </feature_1.default>);
}
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"], ["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"])));
exports.default = MissingPerformanceButtons;
var templateObject_1;
//# sourceMappingURL=missingPerformanceButtons.jsx.map