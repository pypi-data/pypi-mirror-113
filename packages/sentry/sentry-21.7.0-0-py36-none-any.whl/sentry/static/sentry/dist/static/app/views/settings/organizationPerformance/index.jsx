Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var organizations_1 = require("app/actionCreators/organizations");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/organization/permissionAlert"));
var fields = [
    {
        title: locale_1.t('General'),
        fields: [
            {
                name: 'apdexThreshold',
                type: 'number',
                required: true,
                label: locale_1.t('Response Time Threshold (Apdex)'),
                help: locale_1.tct("Set a response time threshold in milliseconds to help define what satisfactory\n                and tolerable response times are. This value will be reflected in the\n                calculation of your [link:Apdex], a standard measurement in performance.", {
                    link: (<externalLink_1.default href="https://docs.sentry.io/performance-monitoring/performance/metrics/#apdex"/>),
                }),
            },
        ],
    },
];
var OrganizationPerformance = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationPerformance, _super);
    function OrganizationPerformance() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSuccess = function (data) {
            organizations_1.updateOrganization(data);
        };
        return _this;
    }
    OrganizationPerformance.prototype.render = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var features = new Set(organization.features);
        var access = new Set(organization.access);
        var endpoint = "/organizations/" + organization.slug + "/";
        var jsonFormSettings = {
            location: location,
            features: features,
            access: access,
            disabled: !(access.has('org:write') && features.has('performance-view')),
        };
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title="Performance"/>
        <permissionAlert_1.default />

        <form_1.default data-test-id="organization-performance-settings" apiMethod="PUT" apiEndpoint={endpoint} saveOnBlur allowUndo initialData={organization} onSubmitSuccess={this.handleSuccess} onSubmitError={function () { return indicator_1.addErrorMessage('Unable to save changes'); }}>
          <jsonForm_1.default {...jsonFormSettings} forms={fields}/>
        </form_1.default>
      </react_1.Fragment>);
    };
    return OrganizationPerformance;
}(react_1.Component));
exports.default = withOrganization_1.default(OrganizationPerformance);
//# sourceMappingURL=index.jsx.map