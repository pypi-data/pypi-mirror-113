Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var hook_1 = tslib_1.__importDefault(require("app/components/hook"));
var sidebarItem_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarItem"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var sidebarDropdownMenu_styled_1 = tslib_1.__importDefault(require("./sidebarDropdownMenu.styled"));
var sidebarMenuItem_1 = tslib_1.__importDefault(require("./sidebarMenuItem"));
var SidebarHelp = function (_a) {
    var orientation = _a.orientation, collapsed = _a.collapsed, hidePanel = _a.hidePanel, organization = _a.organization;
    return (<dropdownMenu_1.default>
    {function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            return (<HelpRoot>
        <HelpActor {...getActorProps({ onClick: hidePanel })}>
          <sidebarItem_1.default data-test-id="help-sidebar" orientation={orientation} collapsed={collapsed} hasPanel={false} icon={<icons_1.IconQuestion size="md"/>} label={locale_1.t('Help')} id="help"/>
        </HelpActor>

        {isOpen && (<HelpMenu {...getMenuProps({})}>
            <sidebarMenuItem_1.default data-test-id="search-docs-and-faqs" onClick={function () { return modal_1.openHelpSearchModal({ organization: organization }); }}>
              {locale_1.t('Search support, docs and more')}
            </sidebarMenuItem_1.default>
            <sidebarMenuItem_1.default href="https://help.sentry.io/">
              {locale_1.t('Visit help center')}
            </sidebarMenuItem_1.default>
            <hook_1.default name="sidebar:help-menu" organization={organization}/>
          </HelpMenu>)}
      </HelpRoot>);
        }}
  </dropdownMenu_1.default>);
};
exports.default = SidebarHelp;
var HelpRoot = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
// This exists to provide a styled actor for the dropdown. Making the actor a regular,
// non-styled react component causes some issues with toggling correctly because of
// how refs are handled.
var HelpActor = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject([""], [""])));
var HelpMenu = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  bottom: 100%;\n"], ["\n  ", ";\n  bottom: 100%;\n"])), sidebarDropdownMenu_styled_1.default);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=help.jsx.map