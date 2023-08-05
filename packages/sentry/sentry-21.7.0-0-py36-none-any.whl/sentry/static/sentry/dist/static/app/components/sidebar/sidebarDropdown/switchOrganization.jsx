Object.defineProperty(exports, "__esModule", { value: true });
exports.SwitchOrganization = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var sidebarDropdownMenu_styled_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarDropdownMenu.styled"));
var sidebarMenuItem_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarMenuItem"));
var sidebarOrgSummary_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarOrgSummary"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var divider_styled_1 = tslib_1.__importDefault(require("./divider.styled"));
/**
 * Switch Organization Menu Label + Sub Menu
 */
var SwitchOrganization = function (_a) {
    var organizations = _a.organizations, canCreateOrganization = _a.canCreateOrganization;
    return (<dropdownMenu_1.default isNestedDropdown>
    {function (_a) {
            var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
            return (<react_1.Fragment>
        <SwitchOrganizationMenuActor data-test-id="sidebar-switch-org" {...getActorProps({})} onClick={function (e) {
                    // This overwrites `DropdownMenu.getActorProps.onClick` which normally handles clicks on actor
                    // to toggle visibility of menu. Instead, do nothing because it is nested and we only want it
                    // to appear when hovered on. Will also stop menu from closing when clicked on (which seems to be common
                    // behavior);
                    // Stop propagation so that dropdown menu doesn't close here
                    e.stopPropagation();
                }}>
          {locale_1.t('Switch organization')}

          <SubMenuCaret>
            <icons_1.IconChevron size="xs" direction="right"/>
          </SubMenuCaret>
        </SwitchOrganizationMenuActor>

        {isOpen && (<SwitchOrganizationMenu data-test-id="sidebar-switch-org-menu" {...getMenuProps({})}>
            <OrganizationList>
              {organizations.map(function (organization) {
                        var url = "/organizations/" + organization.slug + "/";
                        return (<sidebarMenuItem_1.default key={organization.slug} to={url}>
                    <sidebarOrgSummary_1.default organization={organization}/>
                  </sidebarMenuItem_1.default>);
                    })}
            </OrganizationList>
            {organizations && !!organizations.length && canCreateOrganization && (<divider_styled_1.default css={{ marginTop: 0 }}/>)}
            {canCreateOrganization && (<sidebarMenuItem_1.default data-test-id="sidebar-create-org" to="/organizations/new/" style={{ alignItems: 'center' }}>
                <MenuItemLabelWithIcon>
                  <StyledIconAdd />
                  <span>{locale_1.t('Create a new organization')}</span>
                </MenuItemLabelWithIcon>
              </sidebarMenuItem_1.default>)}
          </SwitchOrganizationMenu>)}
      </react_1.Fragment>);
        }}
  </dropdownMenu_1.default>);
};
exports.SwitchOrganization = SwitchOrganization;
var SwitchOrganizationContainer = withOrganizations_1.default(SwitchOrganization);
exports.default = SwitchOrganizationContainer;
var StyledIconAdd = styled_1.default(icons_1.IconAdd)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  color: ", ";\n"], ["\n  margin-right: ", ";\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.gray300; });
var MenuItemLabelWithIcon = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  line-height: 1;\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  line-height: 1;\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"])), space_1.default(1));
var SubMenuCaret = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
// Menu Item in dropdown to "Switch organization"
var SwitchOrganizationMenuActor = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 -", ";\n  padding: 0 ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 -", ";\n  padding: 0 ", ";\n"])), function (p) { return p.theme.sidebar.menuSpacing; }, function (p) { return p.theme.sidebar.menuSpacing; });
var SwitchOrganizationMenu = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n  top: 0;\n  left: 256px;\n"], ["\n  ", ";\n  top: 0;\n  left: 256px;\n"])), sidebarDropdownMenu_styled_1.default);
var OrganizationList = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  max-height: 350px;\n  overflow-y: auto;\n"], ["\n  max-height: 350px;\n  overflow-y: auto;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=switchOrganization.jsx.map