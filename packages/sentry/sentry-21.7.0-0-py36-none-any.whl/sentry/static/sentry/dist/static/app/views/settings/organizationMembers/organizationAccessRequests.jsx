Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var OrganizationAccessRequests = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationAccessRequests, _super);
    function OrganizationAccessRequests() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            accessRequestBusy: {},
        };
        _this.handleApprove = function (id, e) {
            e.stopPropagation();
            _this.handleAction({
                id: id,
                isApproved: true,
                successMessage: locale_1.t('Team request approved'),
                errorMessage: locale_1.t('Error approving team request'),
            });
        };
        _this.handleDeny = function (id, e) {
            e.stopPropagation();
            _this.handleAction({
                id: id,
                isApproved: false,
                successMessage: locale_1.t('Team request denied'),
                errorMessage: locale_1.t('Error denying team request'),
            });
        };
        return _this;
    }
    OrganizationAccessRequests.prototype.handleAction = function (_a) {
        var id = _a.id, isApproved = _a.isApproved, successMessage = _a.successMessage, errorMessage = _a.errorMessage;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _b, api, orgId, onRemoveAccessRequest, _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _b = this.props, api = _b.api, orgId = _b.orgId, onRemoveAccessRequest = _b.onRemoveAccessRequest;
                        this.setState(function (state) {
                            var _a;
                            return ({
                                accessRequestBusy: tslib_1.__assign(tslib_1.__assign({}, state.accessRequestBusy), (_a = {}, _a[id] = true, _a)),
                            });
                        });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/access-requests/" + id + "/", {
                                method: 'PUT',
                                data: { isApproved: isApproved },
                            })];
                    case 2:
                        _d.sent();
                        onRemoveAccessRequest(id);
                        indicator_1.addSuccessMessage(successMessage);
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        indicator_1.addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState(function (state) {
                            var _a;
                            return ({
                                accessRequestBusy: tslib_1.__assign(tslib_1.__assign({}, state.accessRequestBusy), (_a = {}, _a[id] = false, _a)),
                            });
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    OrganizationAccessRequests.prototype.render = function () {
        var _this = this;
        var requestList = this.props.requestList;
        var accessRequestBusy = this.state.accessRequestBusy;
        if (!requestList || !requestList.length) {
            return null;
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Pending Team Requests')}</panels_1.PanelHeader>

        <panels_1.PanelBody>
          {requestList.map(function (_a) {
                var id = _a.id, member = _a.member, team = _a.team, requester = _a.requester;
                var memberName = member.user &&
                    (member.user.name || member.user.email || member.user.username);
                var requesterName = requester && (requester.name || requester.email || requester.username);
                return (<StyledPanelItem key={id}>
                <div data-test-id="request-message">
                  {requesterName
                        ? locale_1.tct('[requesterName] requests to add [name] to the [team] team.', {
                            requesterName: requesterName,
                            name: <strong>{memberName}</strong>,
                            team: <strong>#{team.slug}</strong>,
                        })
                        : locale_1.tct('[name] requests access to the [team] team.', {
                            name: <strong>{memberName}</strong>,
                            team: <strong>#{team.slug}</strong>,
                        })}
                </div>
                <div>
                  <StyledButton priority="primary" size="small" onClick={function (e) { return _this.handleApprove(id, e); }} busy={accessRequestBusy[id]}>
                    {locale_1.t('Approve')}
                  </StyledButton>
                  <button_1.default busy={accessRequestBusy[id]} onClick={function (e) { return _this.handleDeny(id, e); }} size="small">
                    {locale_1.t('Deny')}
                  </button_1.default>
                </div>
              </StyledPanelItem>);
            })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return OrganizationAccessRequests;
}(React.Component));
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(2));
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = withApi_1.default(OrganizationAccessRequests);
var templateObject_1, templateObject_2;
//# sourceMappingURL=organizationAccessRequests.jsx.map