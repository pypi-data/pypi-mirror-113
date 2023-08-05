Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamCreate = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var createTeamForm_1 = tslib_1.__importDefault(require("app/components/teams/createTeamForm"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var TeamCreate = /** @class */ (function (_super) {
    tslib_1.__extends(TeamCreate, _super);
    function TeamCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function (data) {
            var orgId = _this.props.params.orgId;
            var redirectUrl = "/settings/" + orgId + "/teams/" + data.slug + "/";
            _this.props.router.push(redirectUrl);
        };
        return _this;
    }
    TeamCreate.prototype.getTitle = function () {
        return locale_1.t('Create Team');
    };
    TeamCreate.prototype.getEndpoints = function () {
        return [];
    };
    TeamCreate.prototype.renderBody = function () {
        return (<narrowLayout_1.default>
        <h3>{locale_1.t('Create a New Team')}</h3>

        <createTeamForm_1.default onSuccess={this.handleSubmitSuccess} organization={this.props.organization}/>
      </narrowLayout_1.default>);
    };
    return TeamCreate;
}(asyncView_1.default));
exports.TeamCreate = TeamCreate;
exports.default = react_router_1.withRouter(withOrganization_1.default(TeamCreate));
//# sourceMappingURL=teamCreate.jsx.map