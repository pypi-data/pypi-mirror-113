Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var members_1 = require("app/actionCreators/members");
var organizations_1 = require("app/actionCreators/organizations");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var defaultSearchBar_1 = require("app/views/settings/components/defaultSearchBar");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var membersFilter_1 = tslib_1.__importDefault(require("./components/membersFilter"));
var organizationMemberRow_1 = tslib_1.__importDefault(require("./organizationMemberRow"));
var MemberListHeader = hookOrDefault_1.default({
    hookName: 'component:member-list-header',
    defaultComponent: function () { return <panels_1.PanelHeader>{locale_1.t('Members')}</panels_1.PanelHeader>; },
});
var OrganizationMembersList = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationMembersList, _super);
    function OrganizationMembersList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeMember = function (id) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var orgId;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        orgId = this.props.params.orgId;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + orgId + "/members/" + id + "/", {
                                method: 'DELETE',
                                data: {},
                            })];
                    case 1:
                        _a.sent();
                        this.setState(function (state) { return ({
                            members: state.members.filter(function (_a) {
                                var existingId = _a.id;
                                return existingId !== id;
                            }),
                        }); });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleRemove = function (_a) {
            var id = _a.id, name = _a.name;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var organization, orgName, _b;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            organization = this.props.organization;
                            orgName = organization.slug;
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.removeMember(id)];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            indicator_1.addErrorMessage(locale_1.tct('Error removing [name] from [orgName]', { name: name, orgName: orgName }));
                            return [2 /*return*/];
                        case 4:
                            indicator_1.addSuccessMessage(locale_1.tct('Removed [name] from [orgName]', { name: name, orgName: orgName }));
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleLeave = function (_a) {
            var id = _a.id;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var organization, orgName, _b;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            organization = this.props.organization;
                            orgName = organization.slug;
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.removeMember(id)];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            indicator_1.addErrorMessage(locale_1.tct('Error leaving [orgName]', { orgName: orgName }));
                            return [2 /*return*/];
                        case 4:
                            organizations_1.redirectToRemainingOrganization({ orgId: orgName, removeOrg: true });
                            indicator_1.addSuccessMessage(locale_1.tct('You left [orgName]', { orgName: orgName }));
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleSendInvite = function (_a) {
            var id = _a.id, expired = _a.expired;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    invited: tslib_1.__assign(tslib_1.__assign({}, state.invited), (_a = {}, _a[id] = 'loading', _a)),
                                });
                            });
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, members_1.resendMemberInvite(this.api, {
                                    orgId: this.props.params.orgId,
                                    memberId: id,
                                    regenerate: expired,
                                })];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            this.setState(function (state) {
                                var _a;
                                return ({ invited: tslib_1.__assign(tslib_1.__assign({}, state.invited), (_a = {}, _a[id] = null, _a)) });
                            });
                            indicator_1.addErrorMessage(locale_1.t('Error sending invite'));
                            return [2 /*return*/];
                        case 4:
                            this.setState(function (state) {
                                var _a;
                                return ({ invited: tslib_1.__assign(tslib_1.__assign({}, state.invited), (_a = {}, _a[id] = 'success', _a)) });
                            });
                            return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    OrganizationMembersList.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { members: [], invited: {} });
    };
    OrganizationMembersList.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['members', "/organizations/" + orgId + "/members/", {}, { paginate: true }],
            [
                'member',
                "/organizations/" + orgId + "/members/me/",
                {},
                { allowError: function (error) { return error.status === 404; } },
            ],
            [
                'authProvider',
                "/organizations/" + orgId + "/auth-provider/",
                {},
                { allowError: function (error) { return error.status === 403; } },
            ],
        ];
    };
    OrganizationMembersList.prototype.getTitle = function () {
        var orgId = this.props.organization.slug;
        return routeTitle_1.default(locale_1.t('Members'), orgId, false);
    };
    OrganizationMembersList.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, params = _a.params, organization = _a.organization, routes = _a.routes;
        var _b = this.state, membersPageLinks = _b.membersPageLinks, members = _b.members, currentMember = _b.member;
        var orgName = organization.name, access = organization.access;
        var canAddMembers = access.includes('member:write');
        var canRemove = access.includes('member:admin');
        var currentUser = configStore_1.default.get('user');
        // Find out if current user is the only owner
        var isOnlyOwner = !members.find(function (_a) {
            var role = _a.role, email = _a.email, pending = _a.pending;
            return role === 'owner' && email !== currentUser.email && !pending;
        });
        // Only admins/owners can remove members
        var requireLink = !!this.state.authProvider && this.state.authProvider.require_link;
        // eslint-disable-next-line react/prop-types
        var renderSearch = function (_a) {
            var defaultSearchBar = _a.defaultSearchBar, value = _a.value, handleChange = _a.handleChange;
            return (<SearchWrapperWithFilter>
        {defaultSearchBar}
        <dropdownMenu_1.default closeOnEscape>
          {function (_a) {
                    var _b;
                    var getActorProps = _a.getActorProps, isOpen = _a.isOpen;
                    return (<FilterWrapper>
              <button_1.default icon={<icons_1.IconSliders size="xs"/>} {...getActorProps({})}>
                {locale_1.t('Search Filters')}
              </button_1.default>
              {isOpen && (<StyledMembersFilter roles={(_b = currentMember === null || currentMember === void 0 ? void 0 : currentMember.roles) !== null && _b !== void 0 ? _b : constants_1.MEMBER_ROLES} query={value} onChange={function (query) { return handleChange(query); }}/>)}
            </FilterWrapper>);
                }}
        </dropdownMenu_1.default>
      </SearchWrapperWithFilter>);
        };
        return (<React.Fragment>
        <react_1.ClassNames>
          {function (_a) {
                var css = _a.css;
                return _this.renderSearchInput({
                    updateRoute: true,
                    placeholder: locale_1.t('Search Members'),
                    children: renderSearch,
                    className: css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                font-size: ", ";\n              "], ["\n                font-size: ", ";\n              "])), theme_1.default.fontSizeMedium),
                });
            }}
        </react_1.ClassNames>
        <panels_1.Panel data-test-id="org-member-list">
          <MemberListHeader members={members} organization={organization}/>
          <panels_1.PanelBody>
            {members.map(function (member) { return (<organizationMemberRow_1.default routes={routes} params={params} key={member.id} member={member} status={_this.state.invited[member.id]} orgName={orgName} memberCanLeave={!isOnlyOwner} currentUser={currentUser} canRemoveMembers={canRemove} canAddMembers={canAddMembers} requireLink={requireLink} onSendInvite={_this.handleSendInvite} onRemove={_this.handleRemove} onLeave={_this.handleLeave}/>); })}
            {members.length === 0 && (<emptyMessage_1.default>{locale_1.t('No members found.')}</emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <pagination_1.default pageLinks={membersPageLinks}/>
      </React.Fragment>);
    };
    return OrganizationMembersList;
}(asyncView_1.default));
var SearchWrapperWithFilter = styled_1.default(defaultSearchBar_1.SearchWrapper)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n"], ["\n  display: grid;\n"])));
var FilterWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledMembersFilter = styled_1.default(membersFilter_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  right: 0;\n  top: 42px;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    position: absolute;\n    top: -16px;\n    right: 32px;\n    content: '';\n    height: 16px;\n    width: 16px;\n    border: 8px solid transparent;\n    border-bottom-color: ", ";\n  }\n\n  &:before {\n    margin-top: -1px;\n    border-bottom-color: ", ";\n  }\n"], ["\n  position: absolute;\n  right: 0;\n  top: 42px;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    position: absolute;\n    top: -16px;\n    right: 32px;\n    content: '';\n    height: 16px;\n    width: 16px;\n    border: 8px solid transparent;\n    border-bottom-color: ", ";\n  }\n\n  &:before {\n    margin-top: -1px;\n    border-bottom-color: ", ";\n  }\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
exports.default = withOrganization_1.default(OrganizationMembersList);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=organizationMembersList.jsx.map