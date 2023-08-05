Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var activityFeedItem_1 = tslib_1.__importDefault(require("./activityFeedItem"));
var OrganizationActivity = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationActivity, _super);
    function OrganizationActivity() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationActivity.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitle_1.default(locale_1.t('Activity'), orgId);
    };
    OrganizationActivity.prototype.getEndpoints = function () {
        return [['activity', "/organizations/" + this.props.params.orgId + "/activity/"]];
    };
    OrganizationActivity.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationActivity.prototype.renderEmpty = function () {
        return (<emptyStateWarning_1.default>
        <p>{locale_1.t('Nothing to show here, move along.')}</p>
      </emptyStateWarning_1.default>);
    };
    OrganizationActivity.prototype.renderError = function (error, disableLog, disableReport) {
        if (disableLog === void 0) { disableLog = false; }
        if (disableReport === void 0) { disableReport = false; }
        var errors = this.state.errors;
        var notFound = Object.values(errors).find(function (resp) { return resp && resp.status === 404; });
        if (notFound) {
            return this.renderBody();
        }
        return _super.prototype.renderError.call(this, error, disableLog, disableReport);
    };
    OrganizationActivity.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, loading = _a.loading, activity = _a.activity, activityPageLinks = _a.activityPageLinks;
        return (<organization_1.PageContent>
        <pageHeading_1.default withMargins>{locale_1.t('Activity')}</pageHeading_1.default>
        <panels_1.Panel>
          {loading && <loadingIndicator_1.default />}
          {!loading && !(activity === null || activity === void 0 ? void 0 : activity.length) && this.renderEmpty()}
          {!loading && (activity === null || activity === void 0 ? void 0 : activity.length) > 0 && (<div data-test-id="activity-feed-list">
              {activity.map(function (item) { return (<errorBoundary_1.default mini css={{ marginBottom: space_1.default(1), borderRadius: 0 }} key={item.id}>
                  <activityFeedItem_1.default organization={_this.props.organization} item={item}/>
                </errorBoundary_1.default>); })}
            </div>)}
        </panels_1.Panel>
        {activityPageLinks && (<pagination_1.default pageLinks={activityPageLinks} {...this.props}/>)}
      </organization_1.PageContent>);
    };
    return OrganizationActivity;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationActivity);
//# sourceMappingURL=index.jsx.map