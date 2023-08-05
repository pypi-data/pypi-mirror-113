Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var navigationConfiguration_1 = tslib_1.__importDefault(require("app/views/settings/account/navigationConfiguration"));
var settingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsNavigation"));
var AccountSettingsNavigation = function (_a) {
    var organization = _a.organization;
    return (<settingsNavigation_1.default navigationObjects={navigationConfiguration_1.default({ organization: organization })}/>);
};
exports.default = AccountSettingsNavigation;
//# sourceMappingURL=accountSettingsNavigation.jsx.map