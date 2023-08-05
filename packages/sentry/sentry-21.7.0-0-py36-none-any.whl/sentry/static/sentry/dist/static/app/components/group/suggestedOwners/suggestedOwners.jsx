Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var group_1 = require("app/actionCreators/group");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withCommitters_1 = tslib_1.__importDefault(require("app/utils/withCommitters"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var findMatchedRules_1 = require("./findMatchedRules");
var ownershipRules_1 = require("./ownershipRules");
var suggestedAssignees_1 = require("./suggestedAssignees");
var SuggestedOwners = /** @class */ (function (_super) {
    tslib_1.__extends(SuggestedOwners, _super);
    function SuggestedOwners() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            rules: null,
            owners: [],
        };
        _this.fetchOwners = function (eventId) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, data, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/events/" + eventId + "/owners/")];
                    case 2:
                        data = _c.sent();
                        this.setState({
                            rules: data.rules,
                            owners: data.owners,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({
                            rules: null,
                            owners: [],
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleAssign = function (actor) { return function () {
            if (actor.id === undefined) {
                return;
            }
            var event = _this.props.event;
            if (actor.type === 'user') {
                // TODO(ts): `event` here may not be 100% correct
                // in this case groupID should always exist on event
                // since this is only used in Issue Details
                group_1.assignToUser({ id: event.groupID, user: actor });
            }
            if (actor.type === 'team') {
                group_1.assignToActor({ id: event.groupID, actor: actor });
            }
        }; };
        return _this;
    }
    SuggestedOwners.prototype.componentDidMount = function () {
        this.fetchData(this.props.event);
    };
    SuggestedOwners.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.event && prevProps.event) {
            if (this.props.event.id !== prevProps.event.id) {
                // two events, with different IDs
                this.fetchData(this.props.event);
            }
            return;
        }
        if (this.props.event) {
            // going from having no event to having an event
            this.fetchData(this.props.event);
        }
    };
    SuggestedOwners.prototype.fetchData = function (event) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                this.fetchOwners(event.id);
                return [2 /*return*/];
            });
        });
    };
    /**
     * Combine the commiter and ownership data into a single array, merging
     * users who are both owners based on having commits, and owners matching
     * project ownership rules into one array.
     *
     * The return array will include objects of the format:
     *
     * {
     *   actor: <
     *    type,              # Either user or team
     *    SentryTypes.User,  # API expanded user object
     *    {email, id, name}  # Sentry user which is *not* expanded
     *    {email, name}      # Unidentified user (from commits)
     *    {id, name},        # Sentry team (check `type`)
     *   >,
     *
     *   # One or both of commits and rules will be present
     *
     *   commits: [...]  # List of commits made by this owner
     *   rules:   [...]  # Project rules matched for this owner
     * }
     */
    SuggestedOwners.prototype.getOwnerList = function () {
        var _this = this;
        var _a;
        var committers = (_a = this.props.committers) !== null && _a !== void 0 ? _a : [];
        var owners = committers.map(function (commiter) { return ({
            actor: tslib_1.__assign(tslib_1.__assign({}, commiter.author), { type: 'user' }),
            commits: commiter.commits,
        }); });
        this.state.owners.forEach(function (owner) {
            var normalizedOwner = {
                actor: owner,
                rules: findMatchedRules_1.findMatchedRules(_this.state.rules || [], owner),
            };
            var existingIdx = owners.findIndex(function (o) {
                return committers.length === 0 ? o.actor === owner : o.actor.email === owner.email;
            });
            if (existingIdx > -1) {
                owners[existingIdx] = tslib_1.__assign(tslib_1.__assign({}, normalizedOwner), owners[existingIdx]);
                return;
            }
            owners.push(normalizedOwner);
        });
        return owners;
    };
    SuggestedOwners.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, group = _a.group;
        var owners = this.getOwnerList();
        return (<React.Fragment>
        {owners.length > 0 && (<suggestedAssignees_1.SuggestedAssignees owners={owners} onAssign={this.handleAssign}/>)}
        <access_1.default access={['project:write']}>
          <ownershipRules_1.OwnershipRules issueId={group.id} project={project} organization={organization}/>
        </access_1.default>
      </React.Fragment>);
    };
    return SuggestedOwners;
}(React.Component));
exports.default = withApi_1.default(withOrganization_1.default(withCommitters_1.default(SuggestedOwners)));
//# sourceMappingURL=suggestedOwners.jsx.map