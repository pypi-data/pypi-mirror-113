Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var discover_tour_alert_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/discover-tour-alert.svg"));
var discover_tour_explore_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/discover-tour-explore.svg"));
var discover_tour_filter_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/discover-tour-filter.svg"));
var discover_tour_group_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/discover-tour-group.svg"));
var banner_1 = tslib_1.__importDefault(require("app/components/banner"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var featureTourModal_1 = tslib_1.__importStar(require("app/components/modals/featureTourModal"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var useMedia_1 = tslib_1.__importDefault(require("app/utils/useMedia"));
var backgroundSpace_1 = tslib_1.__importDefault(require("./backgroundSpace"));
var docsUrl = 'https://docs.sentry.io/product/discover-queries/';
var docsLink = (<button_1.default external href={docsUrl}>
    {locale_1.t('View Docs')}
  </button_1.default>);
var TOUR_STEPS = [
    {
        title: locale_1.t('Explore Data over Time'),
        image: <featureTourModal_1.TourImage src={discover_tour_explore_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Analyze and visualize all of your data over time to find answers to your most complex problems.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Filter on Event Attributes.'),
        image: <featureTourModal_1.TourImage src={discover_tour_filter_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Drill down on data by any custom tag or field to reduce noise and hone in on specific areas.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Group Data by Tags'),
        image: <featureTourModal_1.TourImage src={discover_tour_group_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Go beyond Issues and create custom groupings to investigate events from a different lens.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Save, Share and Alert'),
        image: <featureTourModal_1.TourImage src={discover_tour_alert_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Send insights to your team and set alerts to monitor any future spikes.')}
      </featureTourModal_1.TourText>),
    },
];
function DiscoverBanner(_a) {
    var organization = _a.organization, resultsUrl = _a.resultsUrl;
    function onAdvance(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'discover_v2.tour.advance',
            eventName: 'Discoverv2: Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    function onCloseModal(step, duration) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'discover_v2.tour.close',
            eventName: 'Discoverv2: Tour Close',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    var isSmallBanner = useMedia_1.default("(max-width: " + theme_1.default.breakpoints[1] + ")");
    return (<banner_1.default title={locale_1.t('Discover Trends')} subtitle={locale_1.t('Customize and save queries by search conditions, event fields, and tags')} backgroundComponent={<backgroundSpace_1.default />} dismissKey="discover">
      <button_1.default size={isSmallBanner ? 'xsmall' : undefined} to={resultsUrl} onClick={function () {
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.build_new_query',
                eventName: 'Discoverv2: Build a new Discover Query',
                organization_id: parseInt(organization.id, 10),
            });
        }}>
        {locale_1.t('Build a new query')}
      </button_1.default>
      <featureTourModal_1.default steps={TOUR_STEPS} doneText={locale_1.t('View all Events')} doneUrl={resultsUrl} onAdvance={onAdvance} onCloseModal={onCloseModal}>
        {function (_a) {
            var showModal = _a.showModal;
            return (<button_1.default size={isSmallBanner ? 'xsmall' : undefined} onClick={function () {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'discover_v2.tour.start',
                        eventName: 'Discoverv2: Tour Start',
                        organization_id: parseInt(organization.id, 10),
                    });
                    showModal();
                }}>
            {locale_1.t('Get a Tour')}
          </button_1.default>);
        }}
      </featureTourModal_1.default>
    </banner_1.default>);
}
exports.default = DiscoverBanner;
//# sourceMappingURL=banner.jsx.map