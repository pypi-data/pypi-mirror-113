Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var collapsible_1 = tslib_1.__importDefault(require("app/components/collapsible"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var projectLink_1 = tslib_1.__importDefault(require("../../list/releaseHealth/projectLink"));
var styles_1 = require("./styles");
function OtherProjects(_a) {
    var projects = _a.projects, location = _a.location, version = _a.version, organization = _a.organization;
    return (<styles_1.Wrapper>
      <styles_1.SectionHeading>
        {locale_1.tn('Other Project for This Release', 'Other Projects for This Release', projects.length)}
      </styles_1.SectionHeading>

      <collapsible_1.default expandButton={function (_a) {
            var onExpand = _a.onExpand, numberOfHiddenItems = _a.numberOfHiddenItems;
            return (<button_1.default priority="link" onClick={onExpand}>
            {locale_1.tn('Show %s collapsed project', 'Show %s collapsed projects', numberOfHiddenItems)}
          </button_1.default>);
        }}>
        {projects.map(function (project) { return (<Row key={project.id}>
            <idBadge_1.default project={project} avatarSize={16}/>
            <projectLink_1.default location={location} orgSlug={organization.slug} releaseVersion={version} project={project}/>
          </Row>); })}
      </collapsible_1.default>
    </styles_1.Wrapper>);
}
var Row = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns: 200px max-content;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns: 200px max-content;\n  }\n"])), space_1.default(0.75), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[1]; }, function (p) {
    return p.theme.breakpoints[2];
});
exports.default = OtherProjects;
var templateObject_1;
//# sourceMappingURL=otherProjects.jsx.map