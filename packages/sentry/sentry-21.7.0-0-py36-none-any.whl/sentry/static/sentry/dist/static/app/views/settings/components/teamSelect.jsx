Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var teamBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/teamBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var TeamSelect = /** @class */ (function (_super) {
    tslib_1.__extends(TeamSelect, _super);
    function TeamSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            teamsSearch: null,
        };
        _this.fetchTeams = debounce_1.default(function (query) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, teamsSearch;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, api.requestPromise("/organizations/" + organization.slug + "/teams/", {
                                query: { query: query, per_page: constants_1.TEAMS_PER_PAGE },
                            })];
                    case 1:
                        teamsSearch = _b.sent();
                        this.setState({ teamsSearch: teamsSearch, loading: false });
                        return [2 /*return*/];
                }
            });
        }); }, constants_1.DEFAULT_DEBOUNCE_DURATION);
        _this.handleQueryUpdate = function (event) {
            _this.setState({ loading: true });
            _this.fetchTeams(event.target.value);
        };
        _this.handleAddTeam = function (option) {
            var _a;
            var team = (_a = _this.state.teamsSearch) === null || _a === void 0 ? void 0 : _a.find(function (tm) { return tm.slug === option.value; });
            if (team) {
                _this.props.onAddTeam(team);
            }
        };
        _this.handleRemove = function (teamSlug) {
            _this.props.onRemoveTeam(teamSlug);
        };
        return _this;
    }
    TeamSelect.prototype.componentDidMount = function () {
        this.fetchTeams();
    };
    TeamSelect.prototype.renderTeamAddDropDown = function () {
        var _a = this.props, disabled = _a.disabled, selectedTeams = _a.selectedTeams, menuHeader = _a.menuHeader;
        var teamsSearch = this.state.teamsSearch;
        var isDisabled = disabled;
        var options = [];
        if (teamsSearch === null || teamsSearch.length === 0) {
            options = [];
        }
        else {
            options = teamsSearch
                .filter(function (team) { return !selectedTeams.some(function (selectedTeam) { return selectedTeam.slug === team.slug; }); })
                .map(function (team, index) { return ({
                index: index,
                value: team.slug,
                searchKey: team.slug,
                label: <DropdownTeamBadge avatarSize={18} team={team}/>,
            }); });
        }
        return (<dropdownAutoComplete_1.default items={options} busyItemsStillVisible={this.state.loading} onChange={this.handleQueryUpdate} onSelect={this.handleAddTeam} emptyMessage={locale_1.t('No teams')} menuHeader={menuHeader} disabled={isDisabled} alignMenu="right">
        {function (_a) {
                var isOpen = _a.isOpen;
                return (<dropdownButton_1.default aria-label={locale_1.t('Add Team')} isOpen={isOpen} size="xsmall" disabled={isDisabled}>
            {locale_1.t('Add Team')}
          </dropdownButton_1.default>);
            }}
      </dropdownAutoComplete_1.default>);
    };
    TeamSelect.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selectedTeams = _a.selectedTeams, disabled = _a.disabled, confirmLastTeamRemoveMessage = _a.confirmLastTeamRemoveMessage;
        if (selectedTeams.length === 0) {
            return <emptyMessage_1.default>{locale_1.t('No Teams assigned')}</emptyMessage_1.default>;
        }
        var confirmMessage = selectedTeams.length === 1 && confirmLastTeamRemoveMessage
            ? confirmLastTeamRemoveMessage
            : null;
        return selectedTeams.map(function (team) { return (<TeamRow key={team.slug} orgId={organization.slug} team={team} onRemove={_this.handleRemove} disabled={disabled} confirmMessage={confirmMessage}/>); });
    };
    TeamSelect.prototype.render = function () {
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          {locale_1.t('Team')}
          {this.renderTeamAddDropDown()}
        </panels_1.PanelHeader>

        <panels_1.PanelBody>{this.renderBody()}</panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return TeamSelect;
}(React.Component));
var TeamRow = function (_a) {
    var orgId = _a.orgId, team = _a.team, onRemove = _a.onRemove, disabled = _a.disabled, confirmMessage = _a.confirmMessage;
    return (<TeamPanelItem>
    <StyledLink to={"/settings/" + orgId + "/teams/" + team.slug + "/"}>
      <teamBadge_1.default team={team}/>
    </StyledLink>
    <confirm_1.default message={confirmMessage} bypass={!confirmMessage} onConfirm={function () { return onRemove(team.slug); }} disabled={disabled}>
      <button_1.default size="xsmall" icon={<icons_1.IconSubtract isCircled size="xs"/>} disabled={disabled}>
        {locale_1.t('Remove')}
      </button_1.default>
    </confirm_1.default>
  </TeamPanelItem>);
};
var DropdownTeamBadge = styled_1.default(teamBadge_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n  font-size: ", ";\n  text-transform: none;\n"], ["\n  font-weight: normal;\n  font-size: ", ";\n  text-transform: none;\n"])), function (p) { return p.theme.fontSizeMedium; });
var TeamPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  align-items: center;\n"], ["\n  padding: ", ";\n  align-items: center;\n"])), space_1.default(2));
var StyledLink = styled_1.default(link_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = withApi_1.default(TeamSelect);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=teamSelect.jsx.map