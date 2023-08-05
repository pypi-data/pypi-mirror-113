Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var settingsLayout_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsLayout"));
var organizationSettingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/organization/organizationSettingsNavigation"));
function OrganizationSettingsLayout(props) {
    return (<settingsLayout_1.default {...props} renderNavigation={function () { return <organizationSettingsNavigation_1.default />; }}/>);
}
exports.default = OrganizationSettingsLayout;
//# sourceMappingURL=organizationSettingsLayout.jsx.map