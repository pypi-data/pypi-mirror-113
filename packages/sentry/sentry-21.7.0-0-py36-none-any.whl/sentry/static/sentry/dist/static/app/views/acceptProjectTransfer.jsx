Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var AcceptProjectTransfer = /** @class */ (function (_super) {
    tslib_1.__extends(AcceptProjectTransfer, _super);
    function AcceptProjectTransfer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (formData) {
            _this.api.request('/accept-transfer/', {
                method: 'POST',
                data: {
                    data: _this.props.location.query.data,
                    organization: formData.organization,
                },
                success: function () {
                    var orgSlug = formData.organization;
                    _this.props.router.push("/" + orgSlug);
                    indicator_1.addSuccessMessage(locale_1.t('Project successfully transferred'));
                },
                error: function (error) {
                    var errorMsg = error && error.responseJSON && typeof error.responseJSON.detail === 'string'
                        ? error.responseJSON.detail
                        : '';
                    indicator_1.addErrorMessage(locale_1.t('Unable to transfer project') + errorMsg ? ": " + errorMsg : '');
                },
            });
        };
        return _this;
    }
    AcceptProjectTransfer.prototype.getEndpoints = function () {
        var query = this.props.location.query;
        return [['transferDetails', '/accept-transfer/', { query: query }]];
    };
    AcceptProjectTransfer.prototype.getTitle = function () {
        return locale_1.t('Accept Project Transfer');
    };
    AcceptProjectTransfer.prototype.renderError = function (error) {
        var disableLog = false;
        // Check if there is an error message with `transferDetails` endpoint
        // If so, show as toast and ignore, otherwise log to sentry
        if (error && error.responseJSON && typeof error.responseJSON.detail === 'string') {
            indicator_1.addErrorMessage(error.responseJSON.detail);
            disableLog = true;
        }
        return _super.prototype.renderError.call(this, error, disableLog);
    };
    AcceptProjectTransfer.prototype.renderBody = function () {
        var _a;
        var transferDetails = this.state.transferDetails;
        var options = transferDetails === null || transferDetails === void 0 ? void 0 : transferDetails.organizations.map(function (org) { return ({
            label: org.slug,
            value: org.slug,
        }); });
        var organization = (_a = options === null || options === void 0 ? void 0 : options[0]) === null || _a === void 0 ? void 0 : _a.value;
        return (<narrowLayout_1.default>
        <settingsPageHeader_1.default title={locale_1.t('Approve Transfer Project Request')}/>
        <p>
          {locale_1.tct('Projects must be transferred to a specific [organization]. ' +
                'You can grant specific teams access to the project later under the [projectSettings]. ' +
                '(Note that granting access to at least one team is necessary for the project to ' +
                'appear in all parts of the UI.)', {
                organization: <strong>{locale_1.t('Organization')}</strong>,
                projectSettings: <strong>{locale_1.t('Project Settings')}</strong>,
            })}
        </p>
        {transferDetails && (<p>
            {locale_1.tct('Please select which [organization] you want for the project [project].', {
                    organization: <strong>{locale_1.t('Organization')}</strong>,
                    project: transferDetails.project.slug,
                })}
          </p>)}
        <form_1.default onSubmit={this.handleSubmit} submitLabel={locale_1.t('Transfer Project')} submitPriority="danger" initialData={organization ? { organization: organization } : undefined}>
          <selectField_1.default options={options} label={locale_1.t('Organization')} name="organization" style={{ borderBottom: 'none' }}/>
        </form_1.default>
      </narrowLayout_1.default>);
    };
    return AcceptProjectTransfer;
}(asyncView_1.default));
exports.default = AcceptProjectTransfer;
//# sourceMappingURL=acceptProjectTransfer.jsx.map