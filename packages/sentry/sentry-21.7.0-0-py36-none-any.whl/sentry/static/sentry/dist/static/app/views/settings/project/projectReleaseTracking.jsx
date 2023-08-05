Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectReleaseTracking = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var pluginList_1 = tslib_1.__importDefault(require("app/components/pluginList"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withPlugins_1 = tslib_1.__importDefault(require("app/utils/withPlugins"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var TOKEN_PLACEHOLDER = 'YOUR_TOKEN';
var WEBHOOK_PLACEHOLDER = 'YOUR_WEBHOOK_URL';
var placeholderData = {
    token: TOKEN_PLACEHOLDER,
    webhookUrl: WEBHOOK_PLACEHOLDER,
};
var ProjectReleaseTracking = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectReleaseTracking, _super);
    function ProjectReleaseTracking() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRegenerateToken = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.api.request("/projects/" + orgId + "/" + projectId + "/releases/token/", {
                method: 'POST',
                data: { project: projectId },
                success: function (data) {
                    _this.setState({
                        data: {
                            token: data.token,
                            webhookUrl: data.webhookUrl,
                        },
                    });
                    indicator_1.addSuccessMessage(locale_1.t('Your deploy token has been regenerated. You will need to update any existing deploy hooks.'));
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.t('Unable to regenerate deploy token, please try again'));
                },
            });
        };
        return _this;
    }
    ProjectReleaseTracking.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Releases'), projectId, false);
    };
    ProjectReleaseTracking.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        // Allow 403s
        return [
            [
                'data',
                "/projects/" + orgId + "/" + projectId + "/releases/token/",
                {},
                { allowError: function (err) { return err && err.status === 403; } },
            ],
        ];
    };
    ProjectReleaseTracking.prototype.getReleaseWebhookIntructions = function () {
        var webhookUrl = (this.state.data || placeholderData).webhookUrl;
        return ('curl ' +
            webhookUrl +
            ' \\' +
            '\n  ' +
            '-X POST \\' +
            '\n  ' +
            "-H 'Content-Type: application/json' \\" +
            '\n  ' +
            '-d \'{"version": "abcdefg"}\'');
    };
    ProjectReleaseTracking.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, plugins = _a.plugins;
        var hasWrite = organization.access.includes('project:write');
        if (plugins.loading) {
            return <loadingIndicator_1.default />;
        }
        var pluginList = plugins.plugins.filter(function (p) { return p.type === 'release-tracking' && p.hasConfiguration; });
        var _b = this.state.data || placeholderData, token = _b.token, webhookUrl = _b.webhookUrl;
        token = getDynamicText_1.default({ value: token, fixed: '__TOKEN__' });
        webhookUrl = getDynamicText_1.default({ value: webhookUrl, fixed: '__WEBHOOK_URL__' });
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Release Tracking')}/>
        {!hasWrite && (<alert_1.default icon={<icons_1.IconFlag size="md"/>} type="warning">
            {locale_1.t('You do not have sufficient permissions to access Release tokens, placeholders are displayed below.')}
          </alert_1.default>)}
        <p>
          {locale_1.t('Configure release tracking for this project to automatically record new releases of your application.')}
        </p>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Client Configuration')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {locale_1.tct('Start by binding the [release] attribute in your application, take a look at [link] to see how to configure this for the SDK you are using.', {
                link: (<a href="https://docs.sentry.io/platform-redirect/?next=/configuration/releases/">
                      our docs
                    </a>),
                release: <code>release</code>,
            })}
            </p>
            <p>
              {locale_1.t("This will annotate each event with the version of your application, as well as automatically create a release entity in the system the first time it's seen.")}
            </p>
            <p>
              {locale_1.t('In addition you may configure a release hook (or use our API) to push a release and include additional metadata with it.')}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Deploy Token')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <field_1.default label={locale_1.t('Token')} help={locale_1.t('A unique secret which is used to generate deploy hook URLs')}>
              <textCopyInput_1.default>{token}</textCopyInput_1.default>
            </field_1.default>
            <field_1.default label={locale_1.t('Regenerate Token')} help={locale_1.t('If a service becomes compromised, you should regenerate the token and re-configure any deploy hooks with the newly generated URL.')}>
              <div>
                <confirm_1.default disabled={!hasWrite} priority="danger" onConfirm={this.handleRegenerateToken} message={locale_1.t('Are you sure you want to regenerate your token? Your current token will no longer be usable.')}>
                  <button_1.default type="button" priority="danger" disabled={!hasWrite}>
                    {locale_1.t('Regenerate Token')}
                  </button_1.default>
                </confirm_1.default>
              </div>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Webhook')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {locale_1.t('If you simply want to integrate with an existing system, sometimes its easiest just to use a webhook.')}
            </p>

            <autoSelectText_1.default>
              <pre>{webhookUrl}</pre>
            </autoSelectText_1.default>

            <p>
              {locale_1.t('The release webhook accepts the same parameters as the "Create a new Release" API endpoint.')}
            </p>

            {getDynamicText_1.default({
                value: (<autoSelectText_1.default>
                  <pre>{this.getReleaseWebhookIntructions()}</pre>
                </autoSelectText_1.default>),
                fixed: (<pre>
                  {"curl __WEBHOOK_URL__ \\\n  -X POST \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"version\": \"abcdefg\"}'"}
                </pre>),
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <pluginList_1.default organization={organization} project={project} pluginList={pluginList}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('API')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {locale_1.t('You can notify Sentry when you release new versions of your application via our HTTP API.')}
            </p>

            <p>
              {locale_1.tct('See the [link:releases documentation] for more information.', {
                link: <a href="https://docs.sentry.io/workflow/releases/"/>,
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return ProjectReleaseTracking;
}(asyncView_1.default));
exports.ProjectReleaseTracking = ProjectReleaseTracking;
exports.default = withPlugins_1.default(ProjectReleaseTracking);
//# sourceMappingURL=projectReleaseTracking.jsx.map