Object.defineProperty(exports, "__esModule", { value: true });
exports.RELEASES_TOUR_STEPS = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var releases_empty_state_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/releases-empty-state.svg"));
var releases_tour_commits_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/releases-tour-commits.svg"));
var releases_tour_email_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/releases-tour-email.svg"));
var releases_tour_resolution_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/releases-tour-resolution.svg"));
var releases_tour_stats_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/releases-tour-stats.svg"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureTourModal_1 = tslib_1.__importStar(require("app/components/modals/featureTourModal"));
var onboardingPanel_1 = tslib_1.__importDefault(require("app/components/onboardingPanel"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var releasesSetupUrl = 'https://docs.sentry.io/product/releases/';
var docsLink = (<button_1.default external href={releasesSetupUrl}>
    {locale_1.t('Setup')}
  </button_1.default>);
exports.RELEASES_TOUR_STEPS = [
    {
        title: locale_1.t('Suspect Commits'),
        image: <featureTourModal_1.TourImage src={releases_tour_commits_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Sentry suggests which commit caused an issue and who is likely responsible so you can triage.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Release Stats'),
        image: <featureTourModal_1.TourImage src={releases_tour_stats_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Get an overview of the commits in each release, and which issues were introduced or fixed.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Easily Resolve'),
        image: <featureTourModal_1.TourImage src={releases_tour_resolution_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Automatically resolve issues by including the issue number in your commit message.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Deploy Emails'),
        image: <featureTourModal_1.TourImage src={releases_tour_email_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Receive email notifications about when your code gets deployed. This can be customized in settings.')}
      </featureTourModal_1.TourText>),
    },
];
var ReleasePromo = /** @class */ (function (_super) {
    tslib_1.__extends(ReleasePromo, _super);
    function ReleasePromo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleTourAdvance = function (step, duration) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'releases.tour.advance',
                eventName: 'Releases: Tour Advance',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step: step,
                duration: duration,
            });
        };
        _this.handleClose = function (step, duration) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'releases.tour.close',
                eventName: 'Releases: Tour Close',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step: step,
                duration: duration,
            });
        };
        return _this;
    }
    ReleasePromo.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'releases.landing_card_viewed',
            eventName: 'Releases: Landing Card Viewed',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId,
        });
    };
    ReleasePromo.prototype.render = function () {
        return (<onboardingPanel_1.default image={<img src={releases_empty_state_svg_1.default}/>}>
        <h3>{locale_1.t('Demystify Releases')}</h3>
        <p>
          {locale_1.t('Did you know how many errors your latest release triggered? We do. And more, too.')}
        </p>
        <ButtonList gap={1}>
          <featureTourModal_1.default steps={exports.RELEASES_TOUR_STEPS} onAdvance={this.handleTourAdvance} onCloseModal={this.handleClose} doneText={locale_1.t('Start Setup')} doneUrl={releasesSetupUrl}>
            {function (_a) {
                var showModal = _a.showModal;
                return (<button_1.default priority="default" onClick={showModal}>
                {locale_1.t('Take a Tour')}
              </button_1.default>);
            }}
          </featureTourModal_1.default>
          <button_1.default priority="primary" href={releasesSetupUrl} external>
            {locale_1.t('Start Setup')}
          </button_1.default>
        </ButtonList>
      </onboardingPanel_1.default>);
    };
    return ReleasePromo;
}(react_1.Component));
var ButtonList = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
exports.default = ReleasePromo;
var templateObject_1;
//# sourceMappingURL=releasePromo.jsx.map