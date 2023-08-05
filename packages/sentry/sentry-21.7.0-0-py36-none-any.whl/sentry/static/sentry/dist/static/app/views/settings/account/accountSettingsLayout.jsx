Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var organizations_1 = require("app/actionCreators/organizations");
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var accountSettingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSettingsNavigation"));
var settingsLayout_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsLayout"));
var AccountSettingsLayout = /** @class */ (function (_super) {
    tslib_1.__extends(AccountSettingsLayout, _super);
    function AccountSettingsLayout() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountSettingsLayout.prototype.getChildContext = function () {
        return {
            organization: this.props.organization,
        };
    };
    AccountSettingsLayout.prototype.componentDidUpdate = function (prevProps) {
        var organization = this.props.organization;
        if (prevProps.organization === organization) {
            return;
        }
        // if there is no org in context, SidebarDropdown uses an org from `withLatestContext`
        // (which queries the org index endpoint instead of org details)
        // and does not have `access` info
        if (organization && typeof organization.access === 'undefined') {
            organizations_1.fetchOrganizationDetails(organization.slug, {
                setActive: true,
                loadProjects: true,
            });
        }
    };
    AccountSettingsLayout.prototype.render = function () {
        var organization = this.props.organization;
        return (<settingsLayout_1.default {...this.props} renderNavigation={function () { return <accountSettingsNavigation_1.default organization={organization}/>; }}>
        {this.props.children}
      </settingsLayout_1.default>);
    };
    AccountSettingsLayout.childContextTypes = {
        organization: sentryTypes_1.default.Organization,
    };
    return AccountSettingsLayout;
}(React.Component));
exports.default = withLatestContext_1.default(AccountSettingsLayout);
//# sourceMappingURL=accountSettingsLayout.jsx.map