Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var contextPickerModal_1 = tslib_1.__importDefault(require("app/components/contextPickerModal"));
function PickProjectToContinue(_a) {
    var noProjectRedirectPath = _a.noProjectRedirectPath, nextPath = _a.nextPath, router = _a.router, projects = _a.projects;
    var nextPathQuery = nextPath.query;
    var navigating = false;
    var path = nextPath.pathname + "?project=";
    if (nextPathQuery) {
        var filteredQuery = Object.entries(nextPathQuery)
            .filter(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], _value = _b[1];
            return key !== 'project';
        })
            .map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
            return key + "=" + value;
        });
        var newPathQuery = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(filteredQuery)), ['project=']).join('&');
        path = nextPath.pathname + "?" + newPathQuery;
    }
    // if the project in URL is missing, but this release belongs to only one project, redirect there
    if (projects.length === 1) {
        router.replace(path + projects[0].id);
        return null;
    }
    modal_1.openModal(function (modalProps) { return (<contextPickerModal_1.default {...modalProps} needOrg={false} needProject nextPath={path + ":project"} onFinish={function (pathname) {
            navigating = true;
            router.replace(pathname);
        }} projectSlugs={projects.map(function (p) { return p.slug; })}/>); }, {
        onClose: function () {
            // we want this to be executed only if the user didn't select any project
            // (closed modal either via button, Esc, clicking outside, ...)
            if (!navigating) {
                router.push(noProjectRedirectPath);
            }
        },
    });
    return <ContextPickerBackground />;
}
var ContextPickerBackground = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 100vh;\n  width: 100%;\n"], ["\n  height: 100vh;\n  width: 100%;\n"])));
exports.default = PickProjectToContinue;
var templateObject_1;
//# sourceMappingURL=pickProjectToContinue.jsx.map