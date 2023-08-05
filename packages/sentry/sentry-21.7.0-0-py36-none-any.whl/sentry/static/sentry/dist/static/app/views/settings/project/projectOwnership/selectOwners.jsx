Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var projects_1 = require("app/actionCreators/projects");
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var multiSelectControl_1 = tslib_1.__importDefault(require("app/components/forms/multiSelectControl"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
function ValueComponent(_a) {
    var data = _a.data, removeProps = _a.removeProps;
    return (<ValueWrapper onClick={removeProps.onClick}>
      <actorAvatar_1.default actor={data.actor} size={28}/>
    </ValueWrapper>);
}
var getSearchKeyForUser = function (user) {
    return (user.email && user.email.toLowerCase()) + " " + (user.name && user.name.toLowerCase());
};
var SelectOwners = /** @class */ (function (_super) {
    tslib_1.__extends(SelectOwners, _super);
    function SelectOwners() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            inputValue: '',
        };
        _this.selectRef = React.createRef();
        _this.renderUserBadge = function (user) { return (<idBadge_1.default avatarSize={24} user={user} hideEmail useLink={false}/>); };
        _this.createMentionableUser = function (user) { return ({
            value: utils_1.buildUserId(user.id),
            label: _this.renderUserBadge(user),
            searchKey: getSearchKeyForUser(user),
            actor: {
                type: 'user',
                id: user.id,
                name: user.name,
            },
        }); };
        _this.createUnmentionableUser = function (_a) {
            var user = _a.user;
            return (tslib_1.__assign(tslib_1.__assign({}, _this.createMentionableUser(user)), { disabled: true, label: (<DisabledLabel>
        <tooltip_1.default position="left" title={locale_1.t('%s is not a member of project', user.name || user.email)}>
          {_this.renderUserBadge(user)}
        </tooltip_1.default>
      </DisabledLabel>) }));
        };
        _this.createMentionableTeam = function (team) { return ({
            value: utils_1.buildTeamId(team.id),
            label: <idBadge_1.default team={team}/>,
            searchKey: "#" + team.slug,
            actor: {
                type: 'team',
                id: team.id,
                name: team.slug,
            },
        }); };
        _this.createUnmentionableTeam = function (team) {
            var organization = _this.props.organization;
            var canAddTeam = organization.access.includes('project:write');
            return tslib_1.__assign(tslib_1.__assign({}, _this.createMentionableTeam(team)), { disabled: true, label: (<Container>
          <DisabledLabel>
            <tooltip_1.default position="left" title={locale_1.t('%s is not a member of project', "#" + team.slug)}>
              <idBadge_1.default team={team}/>
            </tooltip_1.default>
          </DisabledLabel>
          <tooltip_1.default title={canAddTeam
                        ? locale_1.t('Add %s to project', "#" + team.slug)
                        : locale_1.t('You do not have permission to add team to project.')}>
            <AddToProjectButton size="zero" borderless disabled={!canAddTeam} onClick={_this.handleAddTeamToProject.bind(_this, team)} icon={<icons_1.IconAdd isCircled/>}/>
          </tooltip_1.default>
        </Container>) });
        };
        _this.handleChange = function (newValue) {
            _this.props.onChange(newValue);
        };
        _this.handleInputChange = function (inputValue) {
            _this.setState({ inputValue: inputValue });
            if (_this.props.onInputChange) {
                _this.props.onInputChange(inputValue);
            }
        };
        _this.queryMembers = debounce_1.default(function (query, cb) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            // Because this function is debounced, the component can potentially be
            // unmounted before this fires, in which case, `this.api` is null
            if (!api) {
                return null;
            }
            return api
                .requestPromise("/organizations/" + organization.slug + "/members/", {
                query: { query: query },
            })
                .then(function (data) { return cb(null, data); }, function (err) { return cb(err); });
        }, 250);
        _this.handleLoadOptions = function () {
            var usersInProject = _this.getMentionableUsers();
            var teamsInProject = _this.getMentionableTeams();
            var teamsNotInProject = _this.getTeamsNotInProject(teamsInProject);
            var usersInProjectById = usersInProject.map(function (_a) {
                var actor = _a.actor;
                return actor.id;
            });
            // Return a promise for `react-select`
            return new Promise(function (resolve, reject) {
                _this.queryMembers(_this.state.inputValue, function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            })
                .then(function (members) {
                // Be careful here as we actually want the `users` object, otherwise it means user
                // has not registered for sentry yet, but has been invited
                return members
                    ? members
                        .filter(function (_a) {
                        var user = _a.user;
                        return user && usersInProjectById.indexOf(user.id) === -1;
                    })
                        .map(_this.createUnmentionableUser)
                    : [];
            })
                .then(function (members) {
                return tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(usersInProject)), tslib_1.__read(teamsInProject)), tslib_1.__read(teamsNotInProject)), tslib_1.__read(members));
            });
        };
        return _this;
    }
    SelectOwners.prototype.componentDidUpdate = function (prevProps) {
        // Once a team has been added to the project the menu can be closed.
        if (!isEqual_1.default(this.props.projects, prevProps.projects)) {
            this.closeSelectMenu();
        }
    };
    SelectOwners.prototype.getMentionableUsers = function () {
        return memberListStore_1.default.getAll().map(this.createMentionableUser);
    };
    SelectOwners.prototype.getMentionableTeams = function () {
        var project = this.props.project;
        var projectData = projectsStore_1.default.getBySlug(project.slug);
        if (!projectData) {
            return [];
        }
        return projectData.teams.map(this.createMentionableTeam);
    };
    /**
     * Get list of teams that are not in the current project, for use in `MultiSelectMenu`
     */
    SelectOwners.prototype.getTeamsNotInProject = function (teamsInProject) {
        if (teamsInProject === void 0) { teamsInProject = []; }
        var teams = teamStore_1.default.getAll() || [];
        var excludedTeamIds = teamsInProject.map(function (_a) {
            var actor = _a.actor;
            return actor.id;
        });
        return teams
            .filter(function (team) { return excludedTeamIds.indexOf(team.id) === -1; })
            .map(this.createUnmentionableTeam);
    };
    /**
     * Closes the select menu by blurring input if possible since that seems to be the only
     * way to close it.
     */
    SelectOwners.prototype.closeSelectMenu = function () {
        var _a;
        // Close select menu
        if (this.selectRef.current) {
            // eslint-disable-next-line react/no-find-dom-node
            var node = react_dom_1.default.findDOMNode(this.selectRef.current);
            var input = (_a = node) === null || _a === void 0 ? void 0 : _a.querySelector('.Select-input input');
            if (input) {
                // I don't think there's another way to close `react-select`
                input.blur();
            }
        }
    };
    SelectOwners.prototype.handleAddTeamToProject = function (team) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, project, value, oldValue, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, value = _a.value;
                        oldValue = tslib_1.__spreadArray([], tslib_1.__read(value));
                        // Optimistic update
                        this.props.onChange(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.props.value)), [this.createMentionableTeam(team)]));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        // Try to add team to project
                        // Note: we can't close select menu here because we have to wait for ProjectsStore to update first
                        // The reason for this is because we have little control over `react-select`'s `AsyncSelect`
                        // We can't control when `handleLoadOptions` gets called, but it gets called when select closes, so
                        // wait for store to update before closing the menu. Otherwise, we'll have stale items in the select menu
                        return [4 /*yield*/, projects_1.addTeamToProject(api, organization.slug, project.slug, team)];
                    case 2:
                        // Try to add team to project
                        // Note: we can't close select menu here because we have to wait for ProjectsStore to update first
                        // The reason for this is because we have little control over `react-select`'s `AsyncSelect`
                        // We can't control when `handleLoadOptions` gets called, but it gets called when select closes, so
                        // wait for store to update before closing the menu. Otherwise, we'll have stale items in the select menu
                        _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        // Unable to add team to project, revert select menu value
                        this.props.onChange(oldValue);
                        this.closeSelectMenu();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    SelectOwners.prototype.render = function () {
        return (<multiSelectControl_1.default name="owners" filterOption={function (option, filterText) {
                return option.data.searchKey.indexOf(filterText) > -1;
            }} ref={this.selectRef} loadOptions={this.handleLoadOptions} defaultOptions async clearable disabled={this.props.disabled} cache={false} placeholder={locale_1.t('owners')} components={{
                MultiValue: ValueComponent,
            }} onInputChange={this.handleInputChange} onChange={this.handleChange} value={this.props.value} css={{ width: 200 }}/>);
    };
    return SelectOwners;
}(React.Component));
exports.default = withApi_1.default(withProjects_1.default(SelectOwners));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var DisabledLabel = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  opacity: 0.5;\n  overflow: hidden; /* Needed so that \"Add to team\" button can fit */\n"], ["\n  opacity: 0.5;\n  overflow: hidden; /* Needed so that \"Add to team\" button can fit */\n"])));
var AddToProjectButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var ValueWrapper = styled_1.default('a')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=selectOwners.jsx.map