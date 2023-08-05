Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var IntegrationMainSettings = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationMainSettings, _super);
    function IntegrationMainSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            integration: _this.props.integration,
        };
        _this.handleSubmitSuccess = function (data) {
            indicator_1.addSuccessMessage(locale_1.t('Integration updated.'));
            _this.props.onUpdate();
            _this.setState({ integration: data });
        };
        return _this;
    }
    Object.defineProperty(IntegrationMainSettings.prototype, "initialData", {
        get: function () {
            var integration = this.props.integration;
            return {
                name: integration.name,
                domain: integration.domainName || '',
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationMainSettings.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'name',
                    type: 'string',
                    required: false,
                    label: locale_1.t('Integration Name'),
                },
                {
                    name: 'domain',
                    type: 'string',
                    required: false,
                    label: locale_1.t('Full URL'),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationMainSettings.prototype.render = function () {
        var integration = this.state.integration;
        var organization = this.props.organization;
        return (<form_1.default initialData={this.initialData} apiMethod="PUT" apiEndpoint={"/organizations/" + organization.slug + "/integrations/" + integration.id + "/"} onSubmitSuccess={this.handleSubmitSuccess} submitLabel={locale_1.t('Save Settings')}>
        <jsonForm_1.default fields={this.formFields}/>
      </form_1.default>);
    };
    return IntegrationMainSettings;
}(react_1.default.Component));
exports.default = IntegrationMainSettings;
//# sourceMappingURL=integrationMainSettings.jsx.map