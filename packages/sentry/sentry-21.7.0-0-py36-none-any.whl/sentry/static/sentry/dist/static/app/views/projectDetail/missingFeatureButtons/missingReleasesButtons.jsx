Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledButtonBar = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureTourModal_1 = tslib_1.__importDefault(require("app/components/modals/featureTourModal"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var releasePromo_1 = require("app/views/releases/list/releasePromo");
var DOCS_URL = 'https://docs.sentry.io/product/releases/';
var DOCS_HEALTH_URL = 'https://docs.sentry.io/product/releases/health/';
function MissingReleasesButtons(_a) {
    var organization = _a.organization, health = _a.health, projectId = _a.projectId;
    function handleTourAdvance(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'project_detail.releases_tour.advance',
            eventName: 'Project Detail: Releases Tour Advance',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId && parseInt(projectId, 10),
            step: step,
            duration: duration,
        });
    }
    function handleClose(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'project_detail.releases_tour.close',
            eventName: 'Project Detail: Releases Tour Close',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId && parseInt(projectId, 10),
            step: step,
            duration: duration,
        });
    }
    return (<StyledButtonBar gap={1}>
      <button_1.default size="small" priority="primary" external href={health ? DOCS_HEALTH_URL : DOCS_URL}>
        {locale_1.t('Start Setup')}
      </button_1.default>
      {!health && (<featureTourModal_1.default steps={releasePromo_1.RELEASES_TOUR_STEPS} onAdvance={handleTourAdvance} onCloseModal={handleClose} doneText={locale_1.t('Start Setup')} doneUrl={health ? DOCS_HEALTH_URL : DOCS_URL}>
          {function (_a) {
                var showModal = _a.showModal;
                return (<button_1.default size="small" onClick={showModal}>
              {locale_1.t('Get a tour')}
            </button_1.default>);
            }}
        </featureTourModal_1.default>)}
    </StyledButtonBar>);
}
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"], ["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"])));
exports.StyledButtonBar = StyledButtonBar;
exports.default = MissingReleasesButtons;
var templateObject_1;
//# sourceMappingURL=missingReleasesButtons.jsx.map