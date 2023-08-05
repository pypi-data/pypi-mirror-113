Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var badge_1 = tslib_1.__importDefault(require("app/components/badge"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var releaseActions_1 = tslib_1.__importDefault(require("./releaseActions"));
var ReleaseHeader = function (_a) {
    var location = _a.location, organization = _a.organization, release = _a.release, project = _a.project, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    var version = release.version, url = release.url;
    var commitCount = releaseMeta.commitCount, commitFilesChanged = releaseMeta.commitFilesChanged;
    var releasePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(version) + "/";
    var tabs = [
        { title: locale_1.t('Overview'), to: '' },
        {
            title: (<react_1.Fragment>
          {locale_1.t('Commits')} <NavTabsBadge text={formatters_1.formatAbbreviatedNumber(commitCount)}/>
        </react_1.Fragment>),
            to: "commits/",
        },
        {
            title: (<react_1.Fragment>
          {locale_1.t('Files Changed')}
          <NavTabsBadge text={formatters_1.formatAbbreviatedNumber(commitFilesChanged)}/>
        </react_1.Fragment>),
            to: "files-changed/",
        },
    ];
    var getTabUrl = function (path) { return ({
        pathname: releasePath + path,
        query: pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)),
    }); };
    var getActiveTabTo = function () {
        // We are not doing strict version check because there would be a tiny page shift when switching between releases with paginator
        var activeTab = tabs
            .filter(function (tab) { return tab.to.length; }) // remove home 'Overview' from consideration
            .find(function (tab) { return location.pathname.endsWith(tab.to); });
        if (activeTab) {
            return activeTab.to;
        }
        return tabs[0].to; // default to 'Overview'
    };
    return (<Layout.Header>
      <Layout.HeaderContent>
        <breadcrumbs_1.default crumbs={[
            {
                to: "/organizations/" + organization.slug + "/releases/",
                label: locale_1.t('Releases'),
                preserveGlobalSelection: true,
            },
            { label: locale_1.t('Release Details') },
        ]}/>
        <Layout.Title>
          <ReleaseName>
            <idBadge_1.default project={project} avatarSize={28} hideName/>
            <StyledVersion version={version} anchor={false} truncate/>
            <IconWrapper>
              <clipboard_1.default value={version}>
                <tooltip_1.default title={version} containerDisplayMode="flex">
                  <icons_1.IconCopy />
                </tooltip_1.default>
              </clipboard_1.default>
            </IconWrapper>
            {!!url && (<IconWrapper>
                <tooltip_1.default title={url}>
                  <externalLink_1.default href={url}>
                    <icons_1.IconOpen />
                  </externalLink_1.default>
                </tooltip_1.default>
              </IconWrapper>)}
          </ReleaseName>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <releaseActions_1.default organization={organization} projectSlug={project.slug} release={release} releaseMeta={releaseMeta} refetchData={refetchData} location={location}/>
      </Layout.HeaderActions>

      <react_1.Fragment>
        <StyledNavTabs>
          {tabs.map(function (tab) { return (<listLink_1.default key={tab.to} to={getTabUrl(tab.to)} isActive={function () { return getActiveTabTo() === tab.to; }}>
              {tab.title}
            </listLink_1.default>); })}
        </StyledNavTabs>
      </react_1.Fragment>
    </Layout.Header>);
};
var ReleaseName = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledVersion = styled_1.default(version_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var IconWrapper = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"], ["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"])), space_1.default(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
var StyledNavTabs = styled_1.default(navTabs_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"], ["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"])));
var NavTabsBadge = styled_1.default(badge_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
exports.default = ReleaseHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=releaseHeader.jsx.map