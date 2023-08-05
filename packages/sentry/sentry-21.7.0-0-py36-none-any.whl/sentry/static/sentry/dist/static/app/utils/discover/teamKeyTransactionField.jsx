Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var teamKeyTransaction_1 = tslib_1.__importDefault(require("app/components/performance/teamKeyTransaction"));
var TeamKeyTransactionManager = tslib_1.__importStar(require("app/components/performance/teamKeyTransactionsManager"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var utils_1 = require("app/utils");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var TitleStar = /** @class */ (function (_super) {
    tslib_1.__extends(TitleStar, _super);
    function TitleStar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TitleStar.prototype.render = function () {
        var _a, _b;
        var _c = this.props, isOpen = _c.isOpen, keyedTeams = _c.keyedTeams, initialValue = _c.initialValue, props = tslib_1.__rest(_c, ["isOpen", "keyedTeams", "initialValue"]);
        var keyedTeamsCount = (_b = (_a = keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length) !== null && _a !== void 0 ? _a : initialValue) !== null && _b !== void 0 ? _b : 0;
        var star = (<icons_1.IconStar color={keyedTeamsCount ? 'yellow300' : 'gray200'} isSolid={keyedTeamsCount > 0} data-test-id="team-key-transaction-column"/>);
        var button = <button_1.default {...props} icon={star} borderless size="zero"/>;
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
    return TitleStar;
}(react_1.Component));
function TeamKeyTransactionField(_a) {
    var isKeyTransaction = _a.isKeyTransaction, counts = _a.counts, getKeyedTeams = _a.getKeyedTeams, project = _a.project, transactionName = _a.transactionName, props = tslib_1.__rest(_a, ["isKeyTransaction", "counts", "getKeyedTeams", "project", "transactionName"]);
    var keyedTeams = getKeyedTeams(project.id, transactionName);
    return (<teamKeyTransaction_1.default counts={counts} keyedTeams={keyedTeams} title={TitleStar} project={project} transactionName={transactionName} initialValue={Number(isKeyTransaction)} {...props}/>);
}
function TeamKeyTransactionFieldWrapper(_a) {
    var isKeyTransaction = _a.isKeyTransaction, projects = _a.projects, projectSlug = _a.projectSlug, transactionName = _a.transactionName, props = tslib_1.__rest(_a, ["isKeyTransaction", "projects", "projectSlug", "transactionName"]);
    var project = projects.find(function (proj) { return proj.slug === projectSlug; });
    // All these fields need to be defined in order to toggle a team key
    // transaction. Since they are not defined, just render a plain star
    // with no interactions.
    if (!utils_1.defined(project) || !utils_1.defined(transactionName)) {
        return (<TitleStar isOpen={false} disabled keyedTeams={null} initialValue={Number(isKeyTransaction)}/>);
    }
    return (<TeamKeyTransactionManager.Consumer>
      {function (results) { return (<TeamKeyTransactionField isKeyTransaction={isKeyTransaction} project={project} transactionName={transactionName} {...props} {...results}/>); }}
    </TeamKeyTransactionManager.Consumer>);
}
exports.default = withTeams_1.default(withProjects_1.default(TeamKeyTransactionFieldWrapper));
//# sourceMappingURL=teamKeyTransactionField.jsx.map