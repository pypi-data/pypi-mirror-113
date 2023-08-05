Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
function ServiceHookRow(_a) {
    var orgId = _a.orgId, projectId = _a.projectId, hook = _a.hook, onToggleActive = _a.onToggleActive;
    return (<field_1.default label={<react_router_1.Link data-test-id="project-service-hook" to={"/settings/" + orgId + "/projects/" + projectId + "/hooks/" + hook.id + "/"}>
          <truncate_1.default value={hook.url}/>
        </react_router_1.Link>} help={<small>
          {hook.events && hook.events.length !== 0 ? (hook.events.join(', ')) : (<em>{locale_1.t('no events configured')}</em>)}
        </small>}>
      <switchButton_1.default isActive={hook.status === 'active'} size="lg" toggle={onToggleActive}/>
    </field_1.default>);
}
var ProjectServiceHooks = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectServiceHooks, _super);
    function ProjectServiceHooks() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onToggleActive = function (hook) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            var hookList = _this.state.hookList;
            if (!hookList) {
                return;
            }
            indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
            _this.api.request("/projects/" + orgId + "/" + projectId + "/hooks/" + hook.id + "/", {
                method: 'PUT',
                data: {
                    isActive: hook.status !== 'active',
                },
                success: function (data) {
                    indicator_1.clearIndicators();
                    _this.setState({
                        hookList: hookList.map(function (h) {
                            if (h.id === data.id) {
                                return tslib_1.__assign(tslib_1.__assign({}, h), data);
                            }
                            return h;
                        }),
                    });
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.t('Unable to remove application. Please try again.'));
                },
            });
        };
        return _this;
    }
    ProjectServiceHooks.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['hookList', "/projects/" + orgId + "/" + projectId + "/hooks/"]];
    };
    ProjectServiceHooks.prototype.renderEmpty = function () {
        return (<emptyMessage_1.default>
        {locale_1.t('There are no service hooks associated with this project.')}
      </emptyMessage_1.default>);
    };
    ProjectServiceHooks.prototype.renderResults = function () {
        var _this = this;
        var _a;
        var _b = this.props.params, orgId = _b.orgId, projectId = _b.projectId;
        return (<react_1.Fragment>
        <panels_1.PanelHeader key="header">{locale_1.t('Service Hook')}</panels_1.PanelHeader>
        <panels_1.PanelBody key="body">
          <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
            {locale_1.t('Service Hooks are an early adopter preview feature and will change in the future.')}
          </panels_1.PanelAlert>
          {(_a = this.state.hookList) === null || _a === void 0 ? void 0 : _a.map(function (hook) { return (<ServiceHookRow key={hook.id} orgId={orgId} projectId={projectId} hook={hook} onToggleActive={_this.onToggleActive.bind(_this, hook)}/>); })}
        </panels_1.PanelBody>
      </react_1.Fragment>);
    };
    ProjectServiceHooks.prototype.renderBody = function () {
        var hookList = this.state.hookList;
        var body = hookList && hookList.length > 0 ? this.renderResults() : this.renderEmpty();
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var access = new Set(this.props.organization.access);
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Service Hooks')} action={access.has('project:write') ? (<button_1.default data-test-id="new-service-hook" to={"/settings/" + orgId + "/projects/" + projectId + "/hooks/new/"} size="small" priority="primary" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                {locale_1.t('Create New Hook')}
              </button_1.default>) : null}/>
        <panels_1.Panel>{body}</panels_1.Panel>
      </react_1.Fragment>);
    };
    return ProjectServiceHooks;
}(asyncView_1.default));
exports.default = withOrganization_1.default(ProjectServiceHooks);
//# sourceMappingURL=projectServiceHooks.jsx.map