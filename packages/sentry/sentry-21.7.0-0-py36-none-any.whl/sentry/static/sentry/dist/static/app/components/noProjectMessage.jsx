Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
/* TODO: replace with I/O when finished */
var hair_on_fire_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/hair-on-fire.svg"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var NoProjectMessage = /** @class */ (function (_super) {
    tslib_1.__extends(NoProjectMessage, _super);
    function NoProjectMessage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NoProjectMessage.prototype.render = function () {
        var _a = this.props, children = _a.children, organization = _a.organization, projects = _a.projects, loadingProjects = _a.loadingProjects, superuserNeedsToBeProjectMember = _a.superuserNeedsToBeProjectMember;
        var orgId = organization.slug;
        var canCreateProject = organization.access.includes('project:write');
        var canJoinTeam = organization.access.includes('team:read');
        var orgHasProjects;
        var hasProjectAccess;
        if ('projects' in organization) {
            var isSuperuser = configStore_1.default.get('user').isSuperuser;
            orgHasProjects = organization.projects.length > 0;
            hasProjectAccess =
                isSuperuser && !superuserNeedsToBeProjectMember
                    ? organization.projects.some(function (p) { return p.hasAccess; })
                    : organization.projects.some(function (p) { return p.isMember && p.hasAccess; });
        }
        else {
            hasProjectAccess = projects ? projects.length > 0 : false;
            orgHasProjects = hasProjectAccess;
        }
        if (hasProjectAccess || loadingProjects) {
            return children;
        }
        // If the organization has some projects, but the user doesn't have access to
        // those projects, the primary action is to Join a Team. Otherwise the primary
        // action is to create a project.
        var joinTeamAction = (<button_1.default title={canJoinTeam ? undefined : locale_1.t('You do not have permission to join a team.')} disabled={!canJoinTeam} priority={orgHasProjects ? 'primary' : 'default'} to={"/settings/" + orgId + "/teams/"}>
        {locale_1.t('Join a Team')}
      </button_1.default>);
        var createProjectAction = (<button_1.default title={canCreateProject
                ? undefined
                : locale_1.t('You do not have permission to create a project.')} disabled={!canCreateProject} priority={orgHasProjects ? 'default' : 'primary'} to={"/organizations/" + orgId + "/projects/new/"}>
        {locale_1.t('Create project')}
      </button_1.default>);
        return (<Wrapper>
        <HeightWrapper>
          <hair_on_fire_svg_1.default src={hair_on_fire_svg_1.default} height={350} alt="Nothing to see"/>
          <Content>
            <StyledPageHeading>{locale_1.t('Remain Calm')}</StyledPageHeading>
            <HelpMessage>
              {locale_1.t('You need at least one project to use this view')}
            </HelpMessage>
            <Actions gap={1}>
              {!orgHasProjects ? (createProjectAction) : (<react_1.Fragment>
                  {joinTeamAction}
                  {createProjectAction}
                </react_1.Fragment>)}
            </Actions>
          </Content>
        </HeightWrapper>
      </Wrapper>);
    };
    return NoProjectMessage;
}(react_1.Component));
exports.default = NoProjectMessage;
var StyledPageHeading = styled_1.default(pageHeading_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 28px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 28px;\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var HelpMessage = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var Flex = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Wrapper = styled_1.default(Flex)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  align-items: center;\n  justify-content: center;\n"], ["\n  flex: 1;\n  align-items: center;\n  justify-content: center;\n"])));
var HeightWrapper = styled_1.default(Flex)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  height: 350px;\n"], ["\n  height: 350px;\n"])));
var Content = styled_1.default(Flex)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex-direction: column;\n  justify-content: center;\n  margin-left: 40px;\n"], ["\n  flex-direction: column;\n  justify-content: center;\n  margin-left: 40px;\n"])));
var Actions = styled_1.default(buttonBar_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: fit-content;\n"], ["\n  width: fit-content;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=noProjectMessage.jsx.map