var _this = this;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var account_1 = require("app/actionCreators/account");
var demoModeGate_1 = tslib_1.__importDefault(require("app/components/acl/demoModeGate"));
var avatar_1 = tslib_1.__importDefault(require("app/components/avatar"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var hook_1 = tslib_1.__importDefault(require("app/components/hook"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var sidebarDropdownMenu_styled_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarDropdownMenu.styled"));
var sidebarMenuItem_1 = tslib_1.__importStar(require("app/components/sidebar/sidebarMenuItem"));
var sidebarOrgSummary_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarOrgSummary"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var divider_styled_1 = tslib_1.__importDefault(require("./divider.styled"));
var switchOrganization_1 = tslib_1.__importDefault(require("./switchOrganization"));
var SidebarDropdown = function (_a) {
    var _b, _c, _d;
    var api = _a.api, org = _a.org, orientation = _a.orientation, collapsed = _a.collapsed, config = _a.config, user = _a.user, hideOrgLinks = _a.hideOrgLinks;
    var handleLogout = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, account_1.logout(api)];
                case 1:
                    _a.sent();
                    window.location.assign('/auth/login/');
                    return [2 /*return*/];
            }
        });
    }); };
    var hasOrganization = !!org;
    var hasUser = !!user;
    // It's possible we do not have an org in context (e.g. RouteNotFound)
    // Otherwise, we should have the full org
    var hasOrgRead = (_b = org === null || org === void 0 ? void 0 : org.access) === null || _b === void 0 ? void 0 : _b.includes('org:read');
    var hasMemberRead = (_c = org === null || org === void 0 ? void 0 : org.access) === null || _c === void 0 ? void 0 : _c.includes('member:read');
    var hasTeamRead = (_d = org === null || org === void 0 ? void 0 : org.access) === null || _d === void 0 ? void 0 : _d.includes('team:read');
    var canCreateOrg = configStore_1.default.get('features').has('organizations:create');
    // Avatar to use: Organization --> user --> Sentry
    var avatar = hasOrganization || hasUser ? (<StyledAvatar collapsed={collapsed} organization={org} user={!org ? user : undefined} size={32} round={false}/>) : (<SentryLink to="/">
        <icons_1.IconSentry size="32px"/>
      </SentryLink>);
    return (<dropdownMenu_1.default>
      {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            return (<SidebarDropdownRoot {...getRootProps()}>
          <SidebarDropdownActor type="button" data-test-id="sidebar-dropdown" {...getActorProps({})}>
            {avatar}
            {!collapsed && orientation !== 'top' && (<OrgAndUserWrapper>
                <OrgOrUserName>
                  {hasOrganization ? org.name : user.name}{' '}
                  <StyledIconChevron color="white" size="xs" direction="down"/>
                </OrgOrUserName>
                <UserNameOrEmail>
                  {hasOrganization ? user.name : user.email}
                </UserNameOrEmail>
              </OrgAndUserWrapper>)}
          </SidebarDropdownActor>

          {isOpen && (<OrgAndUserMenu {...getMenuProps({})}>
              {hasOrganization && (<react_1.Fragment>
                  <sidebarOrgSummary_1.default organization={org}/>
                  {!hideOrgLinks && (<react_1.Fragment>
                      {hasOrgRead && (<sidebarMenuItem_1.default to={"/settings/" + org.slug + "/"}>
                          {locale_1.t('Organization settings')}
                        </sidebarMenuItem_1.default>)}
                      {hasMemberRead && (<sidebarMenuItem_1.default to={"/settings/" + org.slug + "/members/"}>
                          {locale_1.t('Members')}
                        </sidebarMenuItem_1.default>)}

                      {hasTeamRead && (<sidebarMenuItem_1.default to={"/settings/" + org.slug + "/teams/"}>
                          {locale_1.t('Teams')}
                        </sidebarMenuItem_1.default>)}

                      <hook_1.default name="sidebar:organization-dropdown-menu" organization={org}/>
                    </react_1.Fragment>)}

                  {!config.singleOrganization && (<sidebarMenuItem_1.default>
                      <switchOrganization_1.default canCreateOrganization={canCreateOrg}/>
                    </sidebarMenuItem_1.default>)}
                </react_1.Fragment>)}

              <demoModeGate_1.default>
                {hasOrganization && user && <divider_styled_1.default />}
                {!!user && (<react_1.Fragment>
                    <UserSummary to="/settings/account/details/">
                      <UserBadgeNoOverflow user={user} avatarSize={32}/>
                    </UserSummary>

                    <div>
                      <sidebarMenuItem_1.default to="/settings/account/">
                        {locale_1.t('User settings')}
                      </sidebarMenuItem_1.default>
                      <sidebarMenuItem_1.default to="/settings/account/api/">
                        {locale_1.t('API keys')}
                      </sidebarMenuItem_1.default>
                      <hook_1.default name="sidebar:organization-dropdown-menu-bottom" organization={org}/>
                      {user.isSuperuser && (<sidebarMenuItem_1.default to="/manage/">{locale_1.t('Admin')}</sidebarMenuItem_1.default>)}
                      <sidebarMenuItem_1.default data-test-id="sidebarSignout" onClick={handleLogout}>
                        {locale_1.t('Sign out')}
                      </sidebarMenuItem_1.default>
                    </div>
                  </react_1.Fragment>)}
              </demoModeGate_1.default>
            </OrgAndUserMenu>)}
        </SidebarDropdownRoot>);
        }}
    </dropdownMenu_1.default>);
};
exports.default = withApi_1.default(SidebarDropdown);
var SentryLink = styled_1.default(link_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.white; });
var UserSummary = styled_1.default(link_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n  padding: 10px 15px;\n"], ["\n  ", "\n  padding: 10px 15px;\n"])), function (p) { return sidebarMenuItem_1.menuItemStyles(p); });
var UserBadgeNoOverflow = styled_1.default(idBadge_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var SidebarDropdownRoot = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
// So that long org names and user names do not overflow
var OrgAndUserWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  text-align: left;\n"], ["\n  overflow: hidden;\n  text-align: left;\n"])));
var OrgOrUserName = styled_1.default(textOverflow_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: bold;\n  color: ", ";\n  text-shadow: 0 0 6px rgba(255, 255, 255, 0);\n  transition: 0.15s text-shadow linear;\n"], ["\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: bold;\n  color: ", ";\n  text-shadow: 0 0 6px rgba(255, 255, 255, 0);\n  transition: 0.15s text-shadow linear;\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.white; });
var UserNameOrEmail = styled_1.default(textOverflow_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: 16px;\n  transition: 0.15s color linear;\n"], ["\n  font-size: ", ";\n  line-height: 16px;\n  transition: 0.15s color linear;\n"])), function (p) { return p.theme.fontSizeMedium; });
var SidebarDropdownActor = styled_1.default('button')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  cursor: pointer;\n  border: none;\n  padding: 0;\n  background: none;\n  width: 100%;\n\n  &:hover {\n    ", " {\n      text-shadow: 0 0 6px rgba(255, 255, 255, 0.1);\n    }\n    ", " {\n      color: ", ";\n    }\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  cursor: pointer;\n  border: none;\n  padding: 0;\n  background: none;\n  width: 100%;\n\n  &:hover {\n    ", " {\n      text-shadow: 0 0 6px rgba(255, 255, 255, 0.1);\n    }\n    ", " {\n      color: ", ";\n    }\n  }\n"])), OrgOrUserName, UserNameOrEmail, function (p) { return p.theme.gray200; });
var StyledAvatar = styled_1.default(avatar_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n  margin-right: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.08);\n  border-radius: 6px; /* Fixes background bleeding on corners */\n"], ["\n  margin: ", " 0;\n  margin-right: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.08);\n  border-radius: 6px; /* Fixes background bleeding on corners */\n"])), space_1.default(0.25), function (p) { return (p.collapsed ? '0' : space_1.default(1.5)); });
var OrgAndUserMenu = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  ", ";\n  top: 42px;\n  min-width: 180px;\n  z-index: ", ";\n"], ["\n  ", ";\n  top: 42px;\n  min-width: 180px;\n  z-index: ", ";\n"])), sidebarDropdownMenu_styled_1.default, function (p) { return p.theme.zIndex.orgAndUserMenu; });
var StyledIconChevron = styled_1.default(icons_1.IconChevron)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.25));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=index.jsx.map