Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var locale_1 = require("app/locale");
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var serviceHookSettingsForm_1 = tslib_1.__importDefault(require("app/views/settings/project/serviceHookSettingsForm"));
function ProjectCreateServiceHook(_a) {
    var params = _a.params;
    var orgId = params.orgId, projectId = params.projectId;
    var title = locale_1.t('Create Service Hook');
    return (<react_document_title_1.default title={title + " - Sentry"}>
      <react_1.Fragment>
        <settingsPageHeader_1.default title={title}/>
        <serviceHookSettingsForm_1.default orgId={orgId} projectId={projectId} initialData={{ events: [], isActive: true }}/>
      </react_1.Fragment>
    </react_document_title_1.default>);
}
exports.default = ProjectCreateServiceHook;
//# sourceMappingURL=projectCreateServiceHook.jsx.map