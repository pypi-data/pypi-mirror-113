Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var collapsible_1 = tslib_1.__importDefault(require("app/components/collapsible"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var styles_2 = require("./styles");
function ProjectTeamAccess(_a) {
    var organization = _a.organization, project = _a.project;
    var hasEditPermissions = organization.access.includes('project:write');
    var settingsLink = "/settings/" + organization.slug + "/projects/" + (project === null || project === void 0 ? void 0 : project.slug) + "/teams/";
    function renderInnerBody() {
        if (!project) {
            return <placeholder_1.default height="23px"/>;
        }
        if (project.teams.length === 0) {
            return (<button_1.default to={settingsLink} disabled={!hasEditPermissions} title={hasEditPermissions ? undefined : locale_1.t('You do not have permission to do this')} priority="primary" size="small">
          {locale_1.t('Assign Team')}
        </button_1.default>);
        }
        return (<collapsible_1.default expandButton={function (_a) {
                var onExpand = _a.onExpand, numberOfHiddenItems = _a.numberOfHiddenItems;
                return (<button_1.default priority="link" onClick={onExpand}>
            {locale_1.tn('Show %s collapsed team', 'Show %s collapsed teams', numberOfHiddenItems)}
          </button_1.default>);
            }}>
        {project.teams
                .sort(function (a, b) { return a.slug.localeCompare(b.slug); })
                .map(function (team) { return (<StyledLink to={"/settings/" + organization.slug + "/teams/" + team.slug + "/"} key={team.slug}>
              <idBadge_1.default team={team} hideAvatar/>
            </StyledLink>); })}
      </collapsible_1.default>);
    }
    return (<StyledSidebarSection>
      <styles_2.SectionHeadingWrapper>
        <styles_1.SectionHeading>{locale_1.t('Team Access')}</styles_1.SectionHeading>
        <styles_2.SectionHeadingLink to={settingsLink}>
          <icons_1.IconOpen />
        </styles_2.SectionHeadingLink>
      </styles_2.SectionHeadingWrapper>

      <div>{renderInnerBody()}</div>
    </StyledSidebarSection>);
}
var StyledSidebarSection = styled_1.default(styles_2.SidebarSection)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledLink = styled_1.default(link_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  margin-bottom: ", ";\n"], ["\n  display: block;\n  margin-bottom: ", ";\n"])), space_1.default(0.5));
exports.default = ProjectTeamAccess;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectTeamAccess.jsx.map