Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var CreateTeamAccessRequest = /** @class */ (function (_super) {
    tslib_1.__extends(CreateTeamAccessRequest, _super);
    function CreateTeamAccessRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            createBusy: false,
        };
        _this.handleClick = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, memberId, orgId, teamId, closeModal, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, memberId = _a.memberId, orgId = _a.orgId, teamId = _a.teamId, closeModal = _a.closeModal;
                        this.setState({ createBusy: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/members/" + memberId + "/teams/" + teamId + "/", {
                                method: 'POST',
                            })];
                    case 2:
                        _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Team request sent for approval'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to send team request'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ createBusy: false });
                        closeModal();
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CreateTeamAccessRequest.prototype.render = function () {
        var _a = this.props, Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal, teamId = _a.teamId;
        return (<react_1.Fragment>
        <Body>
          {locale_1.tct('You do not have permission to add members to the #[team] team, but we will send a request to your organization admins for approval.', { team: teamId })}
        </Body>
        <Footer>
          <ButtonGroup>
            <button_1.default onClick={closeModal}>{locale_1.t('Cancel')}</button_1.default>
            <button_1.default priority="primary" onClick={this.handleClick} busy={this.state.createBusy} autoFocus>
              {locale_1.t('Continue')}
            </button_1.default>
          </ButtonGroup>
        </Footer>
      </react_1.Fragment>);
    };
    return CreateTeamAccessRequest;
}(react_1.Component));
var ButtonGroup = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n"])), space_1.default(1));
exports.default = withApi_1.default(CreateTeamAccessRequest);
var templateObject_1;
//# sourceMappingURL=teamAccessRequestModal.jsx.map