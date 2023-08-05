Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var inviteRequestRow_1 = tslib_1.__importDefault(require("./inviteRequestRow"));
var organizationAccessRequests_1 = tslib_1.__importDefault(require("./organizationAccessRequests"));
var OrganizationRequestsView = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationRequestsView, _super);
    function OrganizationRequestsView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAction = function (_a) {
            var inviteRequest = _a.inviteRequest, method = _a.method, data = _a.data, successMessage = _a.successMessage, errorMessage = _a.errorMessage, eventKey = _a.eventKey, eventName = _a.eventName;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b, params, organization, onRemoveInviteRequest, _c;
                return tslib_1.__generator(this, function (_d) {
                    switch (_d.label) {
                        case 0:
                            _b = this.props, params = _b.params, organization = _b.organization, onRemoveInviteRequest = _b.onRemoveInviteRequest;
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    inviteRequestBusy: tslib_1.__assign(tslib_1.__assign({}, state.inviteRequestBusy), (_a = {}, _a[inviteRequest.id] = true, _a)),
                                });
                            });
                            _d.label = 1;
                        case 1:
                            _d.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.api.requestPromise("/organizations/" + params.orgId + "/invite-requests/" + inviteRequest.id + "/", {
                                    method: method,
                                    data: data,
                                })];
                        case 2:
                            _d.sent();
                            onRemoveInviteRequest(inviteRequest.id);
                            indicator_1.addSuccessMessage(successMessage);
                            analytics_1.trackAnalyticsEvent({
                                eventKey: eventKey,
                                eventName: eventName,
                                organization_id: organization.id,
                                member_id: parseInt(inviteRequest.id, 10),
                                invite_status: inviteRequest.inviteStatus,
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            _c = _d.sent();
                            indicator_1.addErrorMessage(errorMessage);
                            return [3 /*break*/, 4];
                        case 4:
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    inviteRequestBusy: tslib_1.__assign(tslib_1.__assign({}, state.inviteRequestBusy), (_a = {}, _a[inviteRequest.id] = false, _a)),
                                });
                            });
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleApprove = function (inviteRequest) {
            _this.handleAction({
                inviteRequest: inviteRequest,
                method: 'PUT',
                data: {
                    role: inviteRequest.role,
                    teams: inviteRequest.teams,
                    approve: 1,
                },
                successMessage: locale_1.tct('[email] has been invited', { email: inviteRequest.email }),
                errorMessage: locale_1.tct('Error inviting [email]', { email: inviteRequest.email }),
                eventKey: 'invite_request.approved',
                eventName: 'Invite Request Approved',
            });
        };
        _this.handleDeny = function (inviteRequest) {
            _this.handleAction({
                inviteRequest: inviteRequest,
                method: 'DELETE',
                data: {},
                successMessage: locale_1.tct('Invite request for [email] denied', {
                    email: inviteRequest.email,
                }),
                errorMessage: locale_1.tct('Error denying invite request for [email]', {
                    email: inviteRequest.email,
                }),
                eventKey: 'invite_request.denied',
                eventName: 'Invite Request Denied',
            });
        };
        return _this;
    }
    OrganizationRequestsView.prototype.getDefaultState = function () {
        var state = _super.prototype.getDefaultState.call(this);
        return tslib_1.__assign(tslib_1.__assign({}, state), { inviteRequestBusy: {} });
    };
    OrganizationRequestsView.prototype.UNSAFE_componentWillMount = function () {
        _super.prototype.UNSAFE_componentWillMount.call(this);
        this.handleRedirect();
    };
    OrganizationRequestsView.prototype.componentDidUpdate = function () {
        this.handleRedirect();
    };
    OrganizationRequestsView.prototype.getEndpoints = function () {
        var orgId = this.props.organization.slug;
        return [['member', "/organizations/" + orgId + "/members/me/"]];
    };
    OrganizationRequestsView.prototype.handleRedirect = function () {
        var _a = this.props, router = _a.router, params = _a.params, requestList = _a.requestList, showInviteRequests = _a.showInviteRequests;
        // redirect to the members view if the user cannot see
        // the invite requests panel and all of the team requests
        // have been approved or denied
        if (showInviteRequests || requestList.length) {
            return null;
        }
        return router.push("/settings/" + params.orgId + "/members/");
    };
    OrganizationRequestsView.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, requestList = _a.requestList, showInviteRequests = _a.showInviteRequests, inviteRequests = _a.inviteRequests, onRemoveAccessRequest = _a.onRemoveAccessRequest, onUpdateInviteRequest = _a.onUpdateInviteRequest, organization = _a.organization, teams = _a.teams;
        var _b = this.state, inviteRequestBusy = _b.inviteRequestBusy, member = _b.member;
        return (<react_1.Fragment>
        {showInviteRequests && (<panels_1.Panel>
            <panels_1.PanelHeader>{locale_1.t('Pending Invite Requests')}</panels_1.PanelHeader>
            <panels_1.PanelBody>
              {inviteRequests.map(function (inviteRequest) { return (<inviteRequestRow_1.default key={inviteRequest.id} organization={organization} inviteRequest={inviteRequest} inviteRequestBusy={inviteRequestBusy} allTeams={teams} allRoles={member ? member.roles : constants_1.MEMBER_ROLES} onApprove={_this.handleApprove} onDeny={_this.handleDeny} onUpdate={function (data) { return onUpdateInviteRequest(inviteRequest.id, data); }}/>); })}
              {inviteRequests.length === 0 && (<emptyMessage_1.default>{locale_1.t('No requests found.')}</emptyMessage_1.default>)}
            </panels_1.PanelBody>
          </panels_1.Panel>)}

        <organizationAccessRequests_1.default orgId={params.orgId} requestList={requestList} onRemoveAccessRequest={onRemoveAccessRequest}/>
      </react_1.Fragment>);
    };
    OrganizationRequestsView.defaultProps = {
        inviteRequests: [],
    };
    return OrganizationRequestsView;
}(asyncView_1.default));
exports.default = withTeams_1.default(withOrganization_1.default(OrganizationRequestsView));
//# sourceMappingURL=organizationRequestsView.jsx.map