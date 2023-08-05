Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var actionLink_1 = tslib_1.__importDefault(require("app/components/actions/actionLink"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var ignore_1 = tslib_1.__importDefault(require("app/components/actions/ignore"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var resolveActions_1 = tslib_1.__importDefault(require("./resolveActions"));
var reviewAction_1 = tslib_1.__importDefault(require("./reviewAction"));
var utils_1 = require("./utils");
function ActionSet(_a) {
    var orgSlug = _a.orgSlug, queryCount = _a.queryCount, query = _a.query, allInQuerySelected = _a.allInQuerySelected, anySelected = _a.anySelected, multiSelected = _a.multiSelected, issues = _a.issues, onUpdate = _a.onUpdate, onShouldConfirm = _a.onShouldConfirm, onDelete = _a.onDelete, onMerge = _a.onMerge, selectedProjectSlug = _a.selectedProjectSlug;
    var numIssues = issues.size;
    var confirm = utils_1.getConfirm(numIssues, allInQuerySelected, query, queryCount);
    var label = utils_1.getLabel(numIssues, allInQuerySelected);
    // merges require a single project to be active in an org context
    // selectedProjectSlug is null when 0 or >1 projects are selected.
    var mergeDisabled = !(multiSelected && selectedProjectSlug);
    var selectedIssues = tslib_1.__spreadArray([], tslib_1.__read(issues)).map(groupStore_1.default.get);
    var canMarkReviewed = anySelected && (allInQuerySelected || selectedIssues.some(function (issue) { return !!(issue === null || issue === void 0 ? void 0 : issue.inbox); }));
    return (<Wrapper>
      {selectedProjectSlug ? (<projects_1.default orgId={orgSlug} slugs={[selectedProjectSlug]}>
          {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
                var selectedProject = projects[0];
                return (<resolveActions_1.default onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
                        hasReleases: selectedProject.hasOwnProperty('features')
                            ? selectedProject.features.includes('releases')
                            : false,
                        latestRelease: selectedProject.hasOwnProperty('latestRelease')
                            ? selectedProject.latestRelease
                            : undefined,
                        projectId: selectedProject.slug,
                        confirm: confirm,
                        label: label,
                        loadingProjects: !initiallyLoaded,
                        projectFetchError: !!fetchError,
                    }}/>);
            }}
        </projects_1.default>) : (<resolveActions_1.default onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
                hasReleases: false,
                latestRelease: null,
                projectId: null,
                confirm: confirm,
                label: label,
            }}/>)}

      <ignore_1.default onUpdate={onUpdate} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.IGNORE)} confirmMessage={confirm(utils_1.ConfirmAction.IGNORE, true)} confirmLabel={label('ignore')} disabled={!anySelected}/>
      <guideAnchor_1.default target="inbox_guide_review" position="bottom">
        <div className="hidden-sm hidden-xs">
          <reviewAction_1.default disabled={!canMarkReviewed} onUpdate={onUpdate}/>
        </div>
      </guideAnchor_1.default>
      <div className="hidden-md hidden-sm hidden-xs">
        <actionLink_1.default type="button" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.MERGE)} message={confirm(utils_1.ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={locale_1.t('Merge Selected Issues')}>
          {locale_1.t('Merge')}
        </actionLink_1.default>
      </div>

      <dropdownLink_1.default key="actions" customTitle={<button_1.default label={locale_1.t('Open more issue actions')} icon={<icons_1.IconEllipsis size="xs"/>}/>}>
        <menuItemActionLink_1.default className="hidden-lg hidden-xl" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.MERGE)} message={confirm(utils_1.ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={locale_1.t('Merge Selected Issues')}>
          {locale_1.t('Merge')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default className="hidden-md hidden-lg hidden-xl" disabled={!canMarkReviewed} onAction={function () { return onUpdate({ inbox: false }); }} title={locale_1.t('Mark Reviewed')}>
          {locale_1.t('Mark Reviewed')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default disabled={!anySelected} onAction={function () { return onUpdate({ isBookmarked: true }); }} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.BOOKMARK)} message={confirm(utils_1.ConfirmAction.BOOKMARK, false)} confirmLabel={label('bookmark')} title={locale_1.t('Add to Bookmarks')}>
          {locale_1.t('Add to Bookmarks')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default disabled={!anySelected} onAction={function () { return onUpdate({ isBookmarked: false }); }} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.UNBOOKMARK)} message={confirm('remove', false, ' from your bookmarks')} confirmLabel={label('remove', ' from your bookmarks')} title={locale_1.t('Remove from Bookmarks')}>
          {locale_1.t('Remove from Bookmarks')}
        </menuItemActionLink_1.default>

        <menuItemActionLink_1.default disabled={!anySelected} onAction={function () { return onUpdate({ status: types_1.ResolutionStatus.UNRESOLVED }); }} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.UNRESOLVE)} message={confirm(utils_1.ConfirmAction.UNRESOLVE, true)} confirmLabel={label('unresolve')} title={locale_1.t('Set status to: Unresolved')}>
          {locale_1.t('Set status to: Unresolved')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default disabled={!anySelected} onAction={onDelete} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.DELETE)} message={confirm(utils_1.ConfirmAction.DELETE, false)} confirmLabel={label('delete')} title={locale_1.t('Delete Issues')}>
          {locale_1.t('Delete Issues')}
        </menuItemActionLink_1.default>
      </dropdownLink_1.default>
    </Wrapper>);
}
exports.default = ActionSet;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin: 0 ", ";\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-start;\n  white-space: nowrap;\n"], ["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin: 0 ", ";\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-start;\n  white-space: nowrap;\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; }, space_1.default(1), space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=actionSet.jsx.map