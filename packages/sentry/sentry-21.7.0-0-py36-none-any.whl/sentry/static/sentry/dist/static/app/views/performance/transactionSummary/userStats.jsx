Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var userMisery_1 = tslib_1.__importDefault(require("app/components/userMisery"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var data_1 = require("app/views/performance/data");
var utils_1 = require("app/views/performance/transactionSummary/transactionVitals/utils");
var utils_2 = require("app/views/performance/transactionSummary/utils");
var vitalInfo_1 = tslib_1.__importDefault(require("../vitalDetail/vitalInfo"));
function UserStats(_a) {
    var eventView = _a.eventView, isLoading = _a.isLoading, hasWebVitals = _a.hasWebVitals, error = _a.error, totals = _a.totals, location = _a.location, organization = _a.organization, transactionName = _a.transactionName;
    var userMisery = error !== null ? <div>{'\u2014'}</div> : <placeholder_1.default height="34px"/>;
    if (!isLoading && error === null && totals) {
        var miserableUsers = void 0, threshold = void 0;
        var userMiseryScore = void 0;
        if (organization.features.includes('project-transaction-threshold')) {
            threshold = totals.project_threshold_config[1];
            miserableUsers = totals.count_miserable_user;
            userMiseryScore = totals.user_misery;
        }
        else {
            threshold = organization.apdexThreshold;
            miserableUsers = totals["count_miserable_user_" + threshold];
            userMiseryScore = totals["user_misery_" + threshold];
        }
        var totalUsers = totals.count_unique_user;
        userMisery = (<userMisery_1.default bars={40} barHeight={30} userMisery={userMiseryScore} miseryLimit={threshold} totalUsers={totalUsers} miserableUsers={miserableUsers}/>);
    }
    var webVitalsTarget = utils_1.vitalsRouteWithQuery({
        orgSlug: organization.slug,
        transaction: transactionName,
        projectID: queryString_1.decodeScalar(location.query.project),
        query: location.query,
    });
    return (<react_1.Fragment>
      {hasWebVitals && (<react_1.Fragment>
          <VitalsHeading>
            <styles_1.SectionHeading>
              {locale_1.t('Web Vitals')}
              <questionTooltip_1.default position="top" title={locale_1.t('Web Vitals with p75 better than the "poor" threshold, as defined by Google Web Vitals.')} size="sm"/>
            </styles_1.SectionHeading>
            <link_1.default to={webVitalsTarget}>
              <icons_1.IconOpen />
            </link_1.default>
          </VitalsHeading>
          <vitalInfo_1.default eventView={eventView} organization={organization} location={location} vital={[fields_1.WebVital.FCP, fields_1.WebVital.LCP, fields_1.WebVital.FID, fields_1.WebVital.CLS]} hideVitalPercentNames hideDurationDetail/>
          <utils_2.SidebarSpacer />
        </react_1.Fragment>)}
      <styles_1.SectionHeading>
        {locale_1.t('User Misery')}
        <questionTooltip_1.default position="top" title={data_1.getTermHelp(organization, organization.features.includes('project-transaction-threshold')
            ? data_1.PERFORMANCE_TERM.USER_MISERY_NEW
            : data_1.PERFORMANCE_TERM.USER_MISERY)} size="sm"/>
      </styles_1.SectionHeading>
      {userMisery}
      <utils_2.SidebarSpacer />
    </react_1.Fragment>);
}
var VitalsHeading = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
exports.default = UserStats;
var templateObject_1;
//# sourceMappingURL=userStats.jsx.map