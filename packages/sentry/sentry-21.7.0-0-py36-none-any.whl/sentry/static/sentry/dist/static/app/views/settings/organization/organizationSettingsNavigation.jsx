Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var settingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsNavigation"));
var navigationConfiguration_1 = tslib_1.__importDefault(require("app/views/settings/organization/navigationConfiguration"));
var OrganizationSettingsNavigation = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationSettingsNavigation, _super);
    function OrganizationSettingsNavigation() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getHooks();
        /**
         * TODO(epurkhiser): Becase the settings organization navigation hooks
         * do not conform to a normal component style hook, and take a single
         * parameter 'organization', we cannot use the `Hook` component here,
         * and must resort to using listening to the HookStore to retrieve hook data.
         *
         * We should update the hook interface for the two hooks used here
         */
        _this.unsubscribe = hookStore_1.default.listen(function (hookName, hooks) {
            _this.handleHooks(hookName, hooks);
        }, undefined);
        return _this;
    }
    OrganizationSettingsNavigation.prototype.componentDidMount = function () {
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState(this.getHooks());
    };
    OrganizationSettingsNavigation.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    OrganizationSettingsNavigation.prototype.getHooks = function () {
        // Allow injection via getsentry et all
        var organization = this.props.organization;
        return {
            hookConfigs: hookStore_1.default.get('settings:organization-navigation-config').map(function (cb) {
                return cb(organization);
            }),
            hooks: hookStore_1.default.get('settings:organization-navigation').map(function (cb) {
                return cb(organization);
            }),
        };
    };
    OrganizationSettingsNavigation.prototype.handleHooks = function (name, hooks) {
        var org = this.props.organization;
        if (name !== 'settings:organization-navigation-config') {
            return;
        }
        this.setState({ hookConfigs: hooks.map(function (cb) { return cb(org); }) });
    };
    OrganizationSettingsNavigation.prototype.render = function () {
        var _a = this.state, hooks = _a.hooks, hookConfigs = _a.hookConfigs;
        var organization = this.props.organization;
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        return (<settingsNavigation_1.default navigationObjects={navigationConfiguration_1.default} access={access} features={features} organization={organization} hooks={hooks} hookConfigs={hookConfigs}/>);
    };
    return OrganizationSettingsNavigation;
}(React.Component));
exports.default = withOrganization_1.default(OrganizationSettingsNavigation);
//# sourceMappingURL=organizationSettingsNavigation.jsx.map