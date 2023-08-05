Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var userFeedback_1 = tslib_1.__importDefault(require("app/data/forms/userFeedback"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var ProjectUserFeedbackSettings = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectUserFeedbackSettings, _super);
    function ProjectUserFeedbackSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            Sentry.showReportDialog({
                // should never make it to the Sentry API, but just in case, use throwaway id
                eventId: '00000000000000000000000000000000',
            });
        };
        return _this;
    }
    ProjectUserFeedbackSettings.prototype.componentDidMount = function () {
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
    };
    ProjectUserFeedbackSettings.prototype.componentWillUnmount = function () {
        window.sentryEmbedCallback = null;
    };
    ProjectUserFeedbackSettings.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [
            ['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"],
            ['project', "/projects/" + orgId + "/" + projectId + "/"],
        ];
    };
    ProjectUserFeedbackSettings.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('User Feedback'), projectId, false);
    };
    ProjectUserFeedbackSettings.prototype.renderBody = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('User Feedback')}/>
        <textBlock_1.default>
          {locale_1.t("Don't rely on stack traces and graphs alone to understand\n            the cause and impact of errors. Enable User Feedback to collect\n            your users' comments when they encounter a crash or bug.")}
        </textBlock_1.default>
        <textBlock_1.default>
          {locale_1.t("When configured, your users will be presented with a dialog prompting\n            them for additional information. That information will get attached to\n            the issue in Sentry.")}
        </textBlock_1.default>
        <ButtonList>
          <button_1.default external href="https://docs.sentry.io/product/user-feedback/">
            {locale_1.t('Read the docs')}
          </button_1.default>
          <button_1.default priority="primary" onClick={this.handleClick}>
            {locale_1.t('Open the report dialog')}
          </button_1.default>
        </ButtonList>

        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint={"/projects/" + orgId + "/" + projectId + "/"} initialData={this.state.project.options}>
          <access_1.default access={['project:write']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return <jsonForm_1.default disabled={!hasAccess} forms={userFeedback_1.default}/>;
        }}
          </access_1.default>
        </form_1.default>
      </div>);
    };
    return ProjectUserFeedbackSettings;
}(asyncView_1.default));
var ButtonList = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(1), space_1.default(2));
exports.default = ProjectUserFeedbackSettings;
var templateObject_1;
//# sourceMappingURL=projectUserFeedback.jsx.map