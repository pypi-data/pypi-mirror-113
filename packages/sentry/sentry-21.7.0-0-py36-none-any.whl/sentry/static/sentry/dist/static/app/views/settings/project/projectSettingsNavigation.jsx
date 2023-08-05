Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var appStoreConnectContext_1 = tslib_1.__importDefault(require("app/components/projects/appStoreConnectContext"));
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
var settingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsNavigation"));
var navigationConfiguration_1 = tslib_1.__importDefault(require("app/views/settings/project/navigationConfiguration"));
var ProjectSettingsNavigation = function (_a) {
    var organization = _a.organization, project = _a.project;
    var appStoreConnectContext = react_1.useContext(appStoreConnectContext_1.default);
    var debugFilesNeedsReview = !!(appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.updateAlertMessage);
    return (<settingsNavigation_1.default navigationObjects={navigationConfiguration_1.default({ project: project, organization: organization, debugFilesNeedsReview: debugFilesNeedsReview })} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} project={project}/>);
};
exports.default = withProject_1.default(ProjectSettingsNavigation);
//# sourceMappingURL=projectSettingsNavigation.jsx.map