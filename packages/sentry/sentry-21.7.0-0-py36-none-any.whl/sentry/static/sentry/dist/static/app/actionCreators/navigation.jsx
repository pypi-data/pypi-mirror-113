Object.defineProperty(exports, "__esModule", { value: true });
exports.setLastRoute = exports.navigateTo = void 0;
var tslib_1 = require("tslib");
var modal_1 = require("app/actionCreators/modal");
var navigationActions_1 = tslib_1.__importDefault(require("app/actions/navigationActions"));
var contextPickerModal_1 = tslib_1.__importDefault(require("app/components/contextPickerModal"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
// TODO(ts): figure out better typing for react-router here
function navigateTo(to, router, configUrl) {
    var _a, _b;
    // Check for placeholder params
    var needOrg = to.indexOf(':orgId') > -1;
    var needProject = to.indexOf(':projectId') > -1;
    var comingFromProjectId = (_b = (_a = router === null || router === void 0 ? void 0 : router.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.project;
    var needProjectId = !comingFromProjectId || Array.isArray(comingFromProjectId);
    var projectById = projectsStore_1.default.getById(comingFromProjectId);
    if (needOrg || (needProject && (needProjectId || !projectById)) || configUrl) {
        modal_1.openModal(function (modalProps) { return (<contextPickerModal_1.default {...modalProps} nextPath={to} needOrg={needOrg} needProject={needProject} configUrl={configUrl} comingFromProjectId={Array.isArray(comingFromProjectId) ? '' : comingFromProjectId || ''} onFinish={function (path) {
                modalProps.closeModal();
                setTimeout(function () { return router.push(path); }, 0);
            }}/>); }, {});
    }
    else {
        projectById
            ? router.push(to.replace(':projectId', projectById.slug))
            : router.push(to);
    }
}
exports.navigateTo = navigateTo;
function setLastRoute(route) {
    navigationActions_1.default.setLastRoute(route);
}
exports.setLastRoute = setLastRoute;
//# sourceMappingURL=navigation.jsx.map