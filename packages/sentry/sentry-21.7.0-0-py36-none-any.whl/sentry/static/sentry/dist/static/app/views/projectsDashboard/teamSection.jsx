Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var projectCard_1 = tslib_1.__importDefault(require("./projectCard"));
var teamMembers_1 = tslib_1.__importDefault(require("./teamMembers"));
var TeamSection = function (_a) {
    var team = _a.team, projects = _a.projects, title = _a.title, showBorder = _a.showBorder, orgId = _a.orgId, access = _a.access;
    var hasTeamAccess = access.has('team:read');
    var hasProjectAccess = access.has('project:read');
    return (<TeamSectionWrapper data-test-id="team" showBorder={showBorder}>
      <TeamTitleBar>
        <TeamName>{title}</TeamName>
        {hasTeamAccess && team && <teamMembers_1.default teamId={team.slug} orgId={orgId}/>}
      </TeamTitleBar>
      <ProjectCards>
        {projects.map(function (project) { return (<projectCard_1.default data-test-id={project.slug} key={project.slug} project={project} hasProjectAccess={hasProjectAccess}/>); })}
      </ProjectCards>
    </TeamSectionWrapper>);
};
var ProjectCards = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[3]; });
var TeamSectionWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-bottom: ", ";\n  padding: 0 ", " ", ";\n"], ["\n  border-bottom: ", ";\n  padding: 0 ", " ", ";\n"])), function (p) { return (p.showBorder ? '1px solid ' + p.theme.border : 0); }, space_1.default(4), space_1.default(4));
var TeamTitleBar = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " 0 ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " 0 ", ";\n"])), space_1.default(3), space_1.default(2));
var TeamName = styled_1.default(pageHeading_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 20px;\n  line-height: 24px; /* We need this so that header doesn't flicker when lazy loading because avatarList height > this */\n"], ["\n  font-size: 20px;\n  line-height: 24px; /* We need this so that header doesn't flicker when lazy loading because avatarList height > this */\n"])));
exports.default = TeamSection;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=teamSection.jsx.map