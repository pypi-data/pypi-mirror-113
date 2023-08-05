Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var organizationAuthList_1 = tslib_1.__importDefault(require("./organizationAuthList"));
var OrganizationAuth = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationAuth, _super);
    function OrganizationAuth() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        _this.handleSendReminders = function (_provider) {
            _this.setState({ sendRemindersBusy: true });
            _this.api.request("/organizations/" + _this.props.params.orgId + "/auth-provider/send-reminders/", {
                method: 'POST',
                data: {},
                success: function () { return indicator_1.addSuccessMessage(locale_1.t('Sent reminders to members')); },
                error: function () { return indicator_1.addErrorMessage(locale_1.t('Failed to send reminders')); },
                complete: function () { return _this.setState({ sendRemindersBusy: false }); },
            });
        };
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        _this.handleConfigure = function (provider) {
            _this.setState({ busy: true });
            _this.api.request("/organizations/" + _this.props.params.orgId + "/auth-provider/", {
                method: 'POST',
                data: { provider: provider, init: true },
                success: function (data) {
                    // Redirect to auth provider URL
                    if (data && data.auth_url) {
                        window.location.href = data.auth_url;
                    }
                },
                error: function () {
                    _this.setState({ busy: false });
                },
            });
        };
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        _this.handleDisableProvider = function (provider) {
            _this.setState({ busy: true });
            _this.api.request("/organizations/" + _this.props.params.orgId + "/auth-provider/", {
                method: 'DELETE',
                data: { provider: provider },
                success: function () {
                    _this.setState({ provider: null, busy: false });
                },
                error: function () {
                    _this.setState({ busy: false });
                },
            });
        };
        return _this;
    }
    OrganizationAuth.prototype.UNSAFE_componentWillUpdate = function (_nextProps, nextState) {
        var access = this.props.organization.access;
        if (nextState.provider && access.includes('org:write')) {
            // If SSO provider is configured, keep showing loading while we redirect
            // to django configuration view
            window.location.assign("/organizations/" + this.props.params.orgId + "/auth/configure/");
        }
    };
    OrganizationAuth.prototype.getEndpoints = function () {
        return [
            ['providerList', "/organizations/" + this.props.params.orgId + "/auth-providers/"],
            ['provider', "/organizations/" + this.props.params.orgId + "/auth-provider/"],
        ];
    };
    OrganizationAuth.prototype.getTitle = function () {
        return routeTitle_1.default(locale_1.t('Auth Settings'), this.props.organization.slug, false);
    };
    OrganizationAuth.prototype.renderBody = function () {
        var _a = this.state, providerList = _a.providerList, provider = _a.provider;
        if (providerList === null) {
            return null;
        }
        if (this.props.organization.access.includes('org:write') && provider) {
            // If SSO provider is configured, keep showing loading while we redirect
            // to django configuration view
            return this.renderLoading();
        }
        var activeProvider = providerList === null || providerList === void 0 ? void 0 : providerList.find(function (p) { return p.key === (provider === null || provider === void 0 ? void 0 : provider.key); });
        return (<organizationAuthList_1.default activeProvider={activeProvider} providerList={providerList}/>);
    };
    return OrganizationAuth;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationAuth);
//# sourceMappingURL=index.jsx.map