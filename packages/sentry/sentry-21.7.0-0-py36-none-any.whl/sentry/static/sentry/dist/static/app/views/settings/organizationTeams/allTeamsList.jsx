Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var allTeamsRow_1 = tslib_1.__importDefault(require("./allTeamsRow"));
function AllTeamsList(_a) {
    var organization = _a.organization, urlPrefix = _a.urlPrefix, openMembership = _a.openMembership, teamList = _a.teamList, access = _a.access;
    var teamNodes = teamList.map(function (team) { return (<allTeamsRow_1.default urlPrefix={urlPrefix} team={team} organization={organization} openMembership={openMembership} key={team.slug}/>); });
    if (!teamNodes.length) {
        var canCreateTeam = access.has('project:admin');
        return (<emptyMessage_1.default>
        {locale_1.tct('No teams here. [teamCreate]', {
                root: <textBlock_1.default noMargin/>,
                teamCreate: canCreateTeam
                    ? locale_1.tct('You can always [link:create one].', {
                        link: (<StyledButton priority="link" onClick={function () {
                                return modal_1.openCreateTeamModal({
                                    organization: organization,
                                });
                            }}/>),
                    })
                    : null,
            })}
      </emptyMessage_1.default>);
    }
    return <react_1.Fragment>{teamNodes}</react_1.Fragment>;
}
exports.default = AllTeamsList;
var StyledButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var templateObject_1;
//# sourceMappingURL=allTeamsList.jsx.map