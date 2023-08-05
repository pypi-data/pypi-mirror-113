Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var apiForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/apiForm"));
var booleanField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/booleanField"));
var multipleCheckbox_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/multipleCheckbox"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var EVENT_CHOICES = ['event.alert', 'event.created'].map(function (e) { return [e, e]; });
var ServiceHookSettingsForm = /** @class */ (function (_super) {
    tslib_1.__extends(ServiceHookSettingsForm, _super);
    function ServiceHookSettingsForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onSubmitSuccess = function () {
            var _a = _this.props, orgId = _a.orgId, projectId = _a.projectId;
            react_router_1.browserHistory.push("/settings/" + orgId + "/projects/" + projectId + "/hooks/");
        };
        return _this;
    }
    ServiceHookSettingsForm.prototype.render = function () {
        var _a = this.props, initialData = _a.initialData, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
        var endpoint = hookId
            ? "/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/"
            : "/projects/" + orgId + "/" + projectId + "/hooks/";
        return (<panels_1.Panel>
        <apiForm_1.default apiMethod={hookId ? 'PUT' : 'POST'} apiEndpoint={endpoint} initialData={initialData} onSubmitSuccess={this.onSubmitSuccess} footerStyle={{
                marginTop: 0,
                paddingRight: 20,
            }} submitLabel={hookId ? locale_1.t('Save Changes') : locale_1.t('Create Hook')}>
          <panels_1.PanelHeader>{locale_1.t('Hook Configuration')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <booleanField_1.default name="isActive" label={locale_1.t('Active')}/>
            <textField_1.default name="url" label={locale_1.t('URL')} required help={locale_1.t('The URL which will receive events.')}/>
            <formField_1.default name="events" label={locale_1.t('Events')} inline={false} help={locale_1.t('The event types you wish to subscribe to.')}>
              {function (_a) {
                var value = _a.value, onChange = _a.onChange;
                return (<multipleCheckbox_1.default onChange={onChange} value={value} choices={EVENT_CHOICES}/>);
            }}
            </formField_1.default>
          </panels_1.PanelBody>
        </apiForm_1.default>
      </panels_1.Panel>);
    };
    return ServiceHookSettingsForm;
}(react_1.Component));
exports.default = ServiceHookSettingsForm;
//# sourceMappingURL=serviceHookSettingsForm.jsx.map