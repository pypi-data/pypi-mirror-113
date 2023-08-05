Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var pluginList_1 = tslib_1.__importDefault(require("app/components/pluginList"));
var projectAlerts_1 = require("app/data/forms/projectAlerts");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var Settings = /** @class */ (function (_super) {
    tslib_1.__extends(Settings, _super);
    function Settings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleEnablePlugin = function (plugin) {
            _this.setState(function (prevState) {
                var _a;
                return ({
                    pluginList: ((_a = prevState.pluginList) !== null && _a !== void 0 ? _a : []).map(function (p) {
                        if (p.id !== plugin.id) {
                            return p;
                        }
                        return tslib_1.__assign(tslib_1.__assign({}, plugin), { enabled: true });
                    }),
                });
            });
        };
        _this.handleDisablePlugin = function (plugin) {
            _this.setState(function (prevState) {
                var _a;
                return ({
                    pluginList: ((_a = prevState.pluginList) !== null && _a !== void 0 ? _a : []).map(function (p) {
                        if (p.id !== plugin.id) {
                            return p;
                        }
                        return tslib_1.__assign(tslib_1.__assign({}, plugin), { enabled: false });
                    }),
                });
            });
        };
        return _this;
    }
    Settings.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { project: null, pluginList: [] });
    };
    Settings.prototype.getProjectEndpoint = function (_a) {
        var orgId = _a.orgId, projectId = _a.projectId;
        return "/projects/" + orgId + "/" + projectId + "/";
    };
    Settings.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var projectEndpoint = this.getProjectEndpoint(params);
        return [
            ['project', projectEndpoint],
            ['pluginList', "/projects/" + orgId + "/" + projectId + "/plugins/"],
        ];
    };
    Settings.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Alerts Settings'), projectId, false);
    };
    Settings.prototype.renderBody = function () {
        var _a = this.props, canEditRule = _a.canEditRule, organization = _a.organization, params = _a.params;
        var orgId = params.orgId;
        var _b = this.state, project = _b.project, pluginList = _b.pluginList;
        if (!project) {
            return null;
        }
        var projectEndpoint = this.getProjectEndpoint(params);
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Alerts Settings')} action={<button_1.default to={{
                    pathname: "/organizations/" + orgId + "/alerts/rules/",
                    query: { project: project.id },
                }} size="small">
              {locale_1.t('View Alert Rules')}
            </button_1.default>}/>
        <permissionAlert_1.default />
        <alertLink_1.default to="/settings/account/notifications/" icon={<icons_1.IconMail />}>
          {locale_1.t('Looking to fine-tune your personal notification preferences? Visit your Account Settings')}
        </alertLink_1.default>

        <form_1.default saveOnBlur allowUndo initialData={{
                subjectTemplate: project.subjectTemplate,
                digestsMinDelay: project.digestsMinDelay,
                digestsMaxDelay: project.digestsMaxDelay,
            }} apiMethod="PUT" apiEndpoint={projectEndpoint}>
          <jsonForm_1.default disabled={!canEditRule} title={locale_1.t('Email Settings')} fields={[projectAlerts_1.fields.subjectTemplate]}/>

          <jsonForm_1.default title={locale_1.t('Digests')} disabled={!canEditRule} fields={[projectAlerts_1.fields.digestsMinDelay, projectAlerts_1.fields.digestsMaxDelay]} renderHeader={function () { return (<panels_1.PanelAlert type="info">
                {locale_1.t('Sentry will automatically digest alerts sent by some services to avoid flooding your inbox with individual issue notifications. To control how frequently notifications are delivered, use the sliders below.')}
              </panels_1.PanelAlert>); }}/>
        </form_1.default>

        {canEditRule && (<pluginList_1.default organization={organization} project={project} pluginList={(pluginList !== null && pluginList !== void 0 ? pluginList : []).filter(function (p) { return p.type === 'notification' && p.hasConfiguration; })} onEnablePlugin={this.handleEnablePlugin} onDisablePlugin={this.handleDisablePlugin}/>)}
      </react_1.Fragment>);
    };
    return Settings;
}(asyncView_1.default));
exports.default = Settings;
//# sourceMappingURL=settings.jsx.map