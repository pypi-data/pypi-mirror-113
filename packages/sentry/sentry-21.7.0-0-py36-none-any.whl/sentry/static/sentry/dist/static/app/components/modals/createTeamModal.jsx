Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var teams_1 = require("app/actionCreators/teams");
var createTeamForm_1 = tslib_1.__importDefault(require("app/components/teams/createTeamForm"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var CreateTeamModal = /** @class */ (function (_super) {
    tslib_1.__extends(CreateTeamModal, _super);
    function CreateTeamModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (data, onSuccess, onError) {
            var _a = _this.props, organization = _a.organization, api = _a.api;
            teams_1.createTeam(api, data, { orgId: organization.slug })
                .then(function (resp) {
                _this.handleSuccess(resp);
                onSuccess(resp);
            })
                .catch(function (err) {
                onError(err);
            });
        };
        return _this;
    }
    CreateTeamModal.prototype.handleSuccess = function (team) {
        if (this.props.onClose) {
            this.props.onClose(team);
        }
        this.props.closeModal();
    };
    CreateTeamModal.prototype.render = function () {
        var _a = this.props, Body = _a.Body, Header = _a.Header, props = tslib_1.__rest(_a, ["Body", "Header"]);
        return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Create Team')}</Header>
        <Body>
          <createTeamForm_1.default {...props} onSubmit={this.handleSubmit}/>
        </Body>
      </react_1.Fragment>);
    };
    return CreateTeamModal;
}(react_1.Component));
exports.default = withApi_1.default(CreateTeamModal);
//# sourceMappingURL=createTeamModal.jsx.map