Object.defineProperty(exports, "__esModule", { value: true });
exports.UserFeedbackEmpty = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var feedback_empty_state_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/feedback-empty-state.svg"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var onboardingPanel_1 = tslib_1.__importDefault(require("app/components/onboardingPanel"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var UserFeedbackEmpty = /** @class */ (function (_super) {
    tslib_1.__extends(UserFeedbackEmpty, _super);
    function UserFeedbackEmpty() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UserFeedbackEmpty.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projectIds = _a.projectIds;
        window.sentryEmbedCallback = function (embed) {
            // Mock the embed's submit xhr to always be successful
            // NOTE: this will not have errors if the form is empty
            embed.submit = function (_body) {
                var _this = this;
                this._submitInProgress = true;
                setTimeout(function () {
                    _this._submitInProgress = false;
                    _this.onSuccess();
                }, 500);
            };
        };
        if (this.hasAnyFeedback === false) {
            // send to reload only due to higher event volume
            analytics_1.trackAdhocEvent({
                eventKey: 'user_feedback.viewed',
                org_id: parseInt(organization.id, 10),
                projects: projectIds,
            });
        }
    };
    UserFeedbackEmpty.prototype.componentWillUnmount = function () {
        window.sentryEmbedCallback = null;
    };
    Object.defineProperty(UserFeedbackEmpty.prototype, "selectedProjects", {
        get: function () {
            var _a = this.props, projects = _a.projects, projectIds = _a.projectIds;
            return projectIds && projectIds.length
                ? projects.filter(function (_a) {
                    var id = _a.id;
                    return projectIds.includes(id);
                })
                : projects;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UserFeedbackEmpty.prototype, "hasAnyFeedback", {
        get: function () {
            return this.selectedProjects.some(function (_a) {
                var hasUserReports = _a.hasUserReports;
                return hasUserReports;
            });
        },
        enumerable: false,
        configurable: true
    });
    UserFeedbackEmpty.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, organization = _b.organization, projectIds = _b.projectIds;
        analytics_1.trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: organization.id,
            projects: projectIds,
        });
    };
    UserFeedbackEmpty.prototype.render = function () {
        var _this = this;
        // Show no user reports if waiting for projects to load or if there is no feedback
        if (this.props.loadingProjects || this.hasAnyFeedback !== false) {
            return (<emptyStateWarning_1.default>
          <p>{locale_1.t('Sorry, no user reports match your filters.')}</p>
        </emptyStateWarning_1.default>);
        }
        // Show landing page after projects have loaded and it is confirmed no projects have feedback
        return (<onboardingPanel_1.default image={<img src={feedback_empty_state_svg_1.default}/>}>
        <h3>{locale_1.t('What do users think?')}</h3>
        <p>
          {locale_1.t("You can't read minds. At least we hope not. Ask users for feedback on the impact of their crashes or bugs and you shall receive.")}
        </p>
        <ButtonList gap={1}>
          <button_1.default external priority="primary" onClick={function () {
                return _this.trackAnalytics({
                    eventKey: 'user_feedback.docs_clicked',
                    eventName: 'User Feedback Docs Clicked',
                });
            }} href="https://docs.sentry.io/product/user-feedback/">
            {locale_1.t('Read the docs')}
          </button_1.default>
          <button_1.default onClick={function () {
                Sentry.showReportDialog({
                    // should never make it to the Sentry API, but just in case, use throwaway id
                    eventId: '00000000000000000000000000000000',
                });
                _this.trackAnalytics({
                    eventKey: 'user_feedback.dialog_opened',
                    eventName: 'User Feedback Dialog Opened',
                });
            }}>
            {locale_1.t('See an example')}
          </button_1.default>
        </ButtonList>
      </onboardingPanel_1.default>);
    };
    return UserFeedbackEmpty;
}(react_1.Component));
exports.UserFeedbackEmpty = UserFeedbackEmpty;
var ButtonList = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
exports.default = withOrganization_1.default(withProjects_1.default(UserFeedbackEmpty));
var templateObject_1;
//# sourceMappingURL=userFeedbackEmpty.jsx.map