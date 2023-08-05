Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var indicator_1 = require("app/actionCreators/indicator");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var serviceHookSettingsForm_1 = tslib_1.__importDefault(require("app/views/settings/project/serviceHookSettingsForm"));
var HookStats = /** @class */ (function (_super) {
    tslib_1.__extends(HookStats, _super);
    function HookStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HookStats.prototype.getEndpoints = function () {
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        var _a = this.props.params, hookId = _a.hookId, orgId = _a.orgId, projectId = _a.projectId;
        return [
            [
                'stats',
                "/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/stats/",
                {
                    query: {
                        since: since,
                        until: until,
                        resolution: '1d',
                    },
                },
            ],
        ];
    };
    HookStats.prototype.renderBody = function () {
        var stats = this.state.stats;
        if (stats === null) {
            return null;
        }
        var emptyStats = true;
        var series = {
            seriesName: locale_1.t('Events'),
            data: stats.map(function (p) {
                if (p.total) {
                    emptyStats = false;
                }
                return {
                    name: p.ts * 1000,
                    value: p.total,
                };
            }),
        };
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Events in the last 30 days (by day)')}</panels_1.PanelHeader>
        <panels_1.PanelBody withPadding>
          {!emptyStats ? (<miniBarChart_1.default isGroupedByDate showTimeInTooltip labelYAxisExtents series={[series]} height={150}/>) : (<emptyMessage_1.default title={locale_1.t('Nothing recorded in the last 30 days.')} description={locale_1.t('Total webhooks fired for this configuration.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return HookStats;
}(asyncComponent_1.default));
var ProjectServiceHookDetails = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectServiceHookDetails, _super);
    function ProjectServiceHookDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onDelete = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
            indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
            _this.api.request("/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/", {
                method: 'DELETE',
                success: function () {
                    indicator_1.clearIndicators();
                    react_router_1.browserHistory.push("/settings/" + orgId + "/projects/" + projectId + "/hooks/");
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.t('Unable to remove application. Please try again.'));
                },
            });
        };
        return _this;
    }
    ProjectServiceHookDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
        return [['hook', "/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/"]];
    };
    ProjectServiceHookDetails.prototype.renderBody = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
        var hook = this.state.hook;
        if (!hook) {
            return null;
        }
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Service Hook Details')}/>

        <errorBoundary_1.default>
          <HookStats params={this.props.params}/>
        </errorBoundary_1.default>

        <serviceHookSettingsForm_1.default orgId={orgId} projectId={projectId} hookId={hookId} initialData={tslib_1.__assign(tslib_1.__assign({}, hook), { isActive: hook.status !== 'disabled' })}/>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Event Validation')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
              Sentry will send the <code>X-ServiceHook-Signature</code> header built using{' '}
              <code>HMAC(SHA256, [secret], [payload])</code>. You should always verify
              this signature before trusting the information provided in the webhook.
            </panels_1.PanelAlert>
            <field_1.default label={locale_1.t('Secret')} flexibleControlStateSize inline={false} help={locale_1.t('The shared secret used for generating event HMAC signatures.')}>
              <textCopyInput_1.default>
                {getDynamicText_1.default({
                value: hook.secret,
                fixed: 'a dynamic secret value',
            })}
              </textCopyInput_1.default>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Delete Hook')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <field_1.default label={locale_1.t('Delete Hook')} help={locale_1.t('Removing this hook is immediate and permanent.')}>
              <div>
                <button_1.default priority="danger" onClick={this.onDelete}>
                  {locale_1.t('Delete Hook')}
                </button_1.default>
              </div>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return ProjectServiceHookDetails;
}(asyncView_1.default));
exports.default = ProjectServiceHookDetails;
//# sourceMappingURL=projectServiceHookDetails.jsx.map