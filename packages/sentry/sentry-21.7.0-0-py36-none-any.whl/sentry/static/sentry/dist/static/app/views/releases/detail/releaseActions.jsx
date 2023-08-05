Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var release_1 = require("app/actionCreators/release");
var api_1 = require("app/api");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var navigationButtonGroup_1 = tslib_1.__importDefault(require("app/components/navigationButtonGroup"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var formatters_1 = require("app/utils/formatters");
var utils_1 = require("../utils");
function ReleaseActions(_a) {
    var location = _a.location, organization = _a.organization, projectSlug = _a.projectSlug, release = _a.release, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    function handleArchive() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, release_1.archiveRelease(new api_1.Client(), {
                                orgSlug: organization.slug,
                                projectSlug: projectSlug,
                                releaseVersion: release.version,
                            })];
                    case 1:
                        _b.sent();
                        react_router_1.browserHistory.push("/organizations/" + organization.slug + "/releases/");
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function handleRestore() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, release_1.restoreRelease(new api_1.Client(), {
                                orgSlug: organization.slug,
                                projectSlug: projectSlug,
                                releaseVersion: release.version,
                            })];
                    case 1:
                        _b.sent();
                        refetchData();
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function getProjectList() {
        var maxVisibleProjects = 5;
        var visibleProjects = releaseMeta.projects.slice(0, maxVisibleProjects);
        var numberOfCollapsedProjects = releaseMeta.projects.length - visibleProjects.length;
        return (<React.Fragment>
        {visibleProjects.map(function (project) { return (<projectBadge_1.default key={project.slug} project={project} avatarSize={18}/>); })}
        {numberOfCollapsedProjects > 0 && (<span>
            <tooltip_1.default title={release.projects
                    .slice(maxVisibleProjects)
                    .map(function (p) { return p.slug; })
                    .join(', ')}>
              + {locale_1.tn('%s other project', '%s other projects', numberOfCollapsedProjects)}
            </tooltip_1.default>
          </span>)}
      </React.Fragment>);
    }
    function getModalHeader(title) {
        return (<h4>
        <textOverflow_1.default>{title}</textOverflow_1.default>
      </h4>);
    }
    function getModalMessage(message) {
        return (<React.Fragment>
        {message}

        <ProjectsWrapper>{getProjectList()}</ProjectsWrapper>

        {locale_1.t('Are you sure you want to do this?')}
      </React.Fragment>);
    }
    function replaceReleaseUrl(toRelease) {
        return toRelease
            ? {
                pathname: location.pathname
                    .replace(encodeURIComponent(release.version), toRelease)
                    .replace(release.version, toRelease),
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { activeRepo: undefined }),
            }
            : '';
    }
    function handleNavigationClick(direction) {
        analytics_1.trackAnalyticsEvent({
            eventKey: "release_detail.pagination",
            eventName: "Release Detail: Pagination",
            organization_id: parseInt(organization.id, 10),
            direction: direction,
        });
    }
    var _b = release.currentProjectMeta, nextReleaseVersion = _b.nextReleaseVersion, prevReleaseVersion = _b.prevReleaseVersion, firstReleaseVersion = _b.firstReleaseVersion, lastReleaseVersion = _b.lastReleaseVersion;
    return (<buttonBar_1.default gap={1}>
      <navigationButtonGroup_1.default hasPrevious={!!prevReleaseVersion} hasNext={!!nextReleaseVersion} links={[
            replaceReleaseUrl(firstReleaseVersion),
            replaceReleaseUrl(prevReleaseVersion),
            replaceReleaseUrl(nextReleaseVersion),
            replaceReleaseUrl(lastReleaseVersion),
        ]} onOldestClick={function () { return handleNavigationClick('oldest'); }} onOlderClick={function () { return handleNavigationClick('older'); }} onNewerClick={function () { return handleNavigationClick('newer'); }} onNewestClick={function () { return handleNavigationClick('newest'); }}/>
      <StyledDropdownLink caret={false} anchorRight={window.innerWidth > 992} title={<ActionsButton icon={<icons_1.IconEllipsis />} label={locale_1.t('Actions')}/>}>
        {utils_1.isReleaseArchived(release) ? (<confirm_1.default onConfirm={handleRestore} header={getModalHeader(locale_1.tct('Restore Release [release]', {
                release: formatters_1.formatVersion(release.version),
            }))} message={getModalMessage(locale_1.tn('You are restoring this release for the following project:', 'By restoring this release, you are also restoring it for the following projects:', releaseMeta.projects.length))} cancelText={locale_1.t('Nevermind')} confirmText={locale_1.t('Restore')}>
            <menuItem_1.default>{locale_1.t('Restore')}</menuItem_1.default>
          </confirm_1.default>) : (<confirm_1.default onConfirm={handleArchive} header={getModalHeader(locale_1.tct('Archive Release [release]', {
                release: formatters_1.formatVersion(release.version),
            }))} message={getModalMessage(locale_1.tn('You are archiving this release for the following project:', 'By archiving this release, you are also archiving it for the following projects:', releaseMeta.projects.length))} cancelText={locale_1.t('Nevermind')} confirmText={locale_1.t('Archive')}>
            <menuItem_1.default>{locale_1.t('Archive')}</menuItem_1.default>
          </confirm_1.default>)}
      </StyledDropdownLink>
    </buttonBar_1.default>);
}
var ActionsButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 40px;\n  height: 40px;\n  padding: 0;\n"], ["\n  width: 40px;\n  height: 40px;\n  padding: 0;\n"])));
var StyledDropdownLink = styled_1.default(dropdownLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  & + .dropdown-menu {\n    top: 50px !important;\n  }\n"], ["\n  & + .dropdown-menu {\n    top: 50px !important;\n  }\n"])));
var ProjectsWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0 ", " ", ";\n  display: grid;\n  gap: ", ";\n  img {\n    border: none !important;\n    box-shadow: none !important;\n  }\n"], ["\n  margin: ", " 0 ", " ", ";\n  display: grid;\n  gap: ", ";\n  img {\n    border: none !important;\n    box-shadow: none !important;\n  }\n"])), space_1.default(2), space_1.default(2), space_1.default(2), space_1.default(0.5));
exports.default = ReleaseActions;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseActions.jsx.map