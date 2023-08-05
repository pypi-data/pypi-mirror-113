Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var resolve_1 = tslib_1.__importDefault(require("app/components/actions/resolve"));
var utils_1 = require("./utils");
function ResolveActionsContainer(_a) {
    var params = _a.params, orgSlug = _a.orgSlug, anySelected = _a.anySelected, onShouldConfirm = _a.onShouldConfirm, onUpdate = _a.onUpdate;
    var hasReleases = params.hasReleases, latestRelease = params.latestRelease, projectId = params.projectId, confirm = params.confirm, label = params.label, loadingProjects = params.loadingProjects, projectFetchError = params.projectFetchError;
    // resolve requires a single project to be active in an org context
    // projectId is null when 0 or >1 projects are selected.
    var resolveDisabled = Boolean(!anySelected || projectFetchError);
    var resolveDropdownDisabled = Boolean(!anySelected || !projectId || loadingProjects || projectFetchError);
    return (<resolve_1.default hasRelease={hasReleases} latestRelease={latestRelease} orgSlug={orgSlug} projectSlug={projectId} onUpdate={onUpdate} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.RESOLVE)} confirmMessage={confirm('resolve', true)} confirmLabel={label('resolve')} disabled={resolveDisabled} disableDropdown={resolveDropdownDisabled} projectFetchError={projectFetchError}/>);
}
exports.default = ResolveActionsContainer;
//# sourceMappingURL=resolveActions.jsx.map