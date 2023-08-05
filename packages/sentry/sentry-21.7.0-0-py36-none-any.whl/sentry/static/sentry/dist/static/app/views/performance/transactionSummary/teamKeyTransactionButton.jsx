Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var teamKeyTransaction_1 = tslib_1.__importDefault(require("app/components/performance/teamKeyTransaction"));
var TeamKeyTransactionManager = tslib_1.__importStar(require("app/components/performance/teamKeyTransactionsManager"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
/**
 * This can't be a function component because `TeamKeyTransaction` uses
 * `DropdownControl` which in turn uses passes a ref to this component.
 */
var TitleButton = /** @class */ (function (_super) {
    tslib_1.__extends(TitleButton, _super);
    function TitleButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TitleButton.prototype.render = function () {
        var _a;
        var _b = this.props, isOpen = _b.isOpen, keyedTeams = _b.keyedTeams, props = tslib_1.__rest(_b, ["isOpen", "keyedTeams"]);
        var keyedTeamsCount = (_a = keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length) !== null && _a !== void 0 ? _a : 0;
        var button = (<button_1.default {...props} icon={keyedTeamsCount ? <icons_1.IconStar color="yellow300" isSolid/> : <icons_1.IconStar />}>
        {keyedTeamsCount
                ? locale_1.tn('Starred for Team', 'Starred for Teams', keyedTeamsCount)
                : locale_1.t('Star for Team')}
      </button_1.default>);
        if (!isOpen && (keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length)) {
            var teamSlugs = keyedTeams.map(function (_a) {
                var slug = _a.slug;
                return slug;
            }).join(', ');
            return <tooltip_1.default title={teamSlugs}>{button}</tooltip_1.default>;
        }
        else {
            return button;
        }
    };
    return TitleButton;
}(react_1.Component));
function TeamKeyTransactionButton(_a) {
    var counts = _a.counts, getKeyedTeams = _a.getKeyedTeams, project = _a.project, transactionName = _a.transactionName, props = tslib_1.__rest(_a, ["counts", "getKeyedTeams", "project", "transactionName"]);
    var keyedTeams = getKeyedTeams(project.id, transactionName);
    return (<teamKeyTransaction_1.default counts={counts} keyedTeams={keyedTeams} title={TitleButton} project={project} transactionName={transactionName} {...props}/>);
}
function TeamKeyTransactionButtonWrapper(_a) {
    var eventView = _a.eventView, organization = _a.organization, teams = _a.teams, projects = _a.projects, props = tslib_1.__rest(_a, ["eventView", "organization", "teams", "projects"]);
    if (eventView.project.length !== 1) {
        return <TitleButton isOpen={false} disabled keyedTeams={null}/>;
    }
    var projectId = String(eventView.project[0]);
    var project = projects.find(function (proj) { return proj.id === projectId; });
    if (!utils_1.defined(project)) {
        return <TitleButton isOpen={false} disabled keyedTeams={null}/>;
    }
    var isSuperuser = isActiveSuperuser_1.isActiveSuperuser();
    var userTeams = teams.filter(function (_a) {
        var isMember = _a.isMember;
        return isMember || isSuperuser;
    });
    return (<TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={[String(projectId)]}>
      <TeamKeyTransactionManager.Consumer>
        {function (results) { return (<TeamKeyTransactionButton organization={organization} project={project} {...props} {...results}/>); }}
      </TeamKeyTransactionManager.Consumer>
    </TeamKeyTransactionManager.Provider>);
}
exports.default = withTeams_1.default(withProjects_1.default(TeamKeyTransactionButtonWrapper));
//# sourceMappingURL=teamKeyTransactionButton.jsx.map