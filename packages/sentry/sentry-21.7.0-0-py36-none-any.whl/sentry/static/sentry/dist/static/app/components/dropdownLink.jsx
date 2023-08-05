Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var icons_1 = require("app/icons");
var getRootCss = function (theme) { return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  .dropdown-menu {\n    & > li > a {\n      color: ", ";\n\n      &:hover,\n      &:focus {\n        color: inherit;\n        background-color: ", ";\n      }\n    }\n\n    & .disabled {\n      cursor: not-allowed;\n      &:hover {\n        background: inherit;\n        color: inherit;\n      }\n    }\n  }\n\n  .dropdown-submenu:hover > span {\n    color: ", ";\n    background: ", ";\n  }\n"], ["\n  .dropdown-menu {\n    & > li > a {\n      color: ", ";\n\n      &:hover,\n      &:focus {\n        color: inherit;\n        background-color: ", ";\n      }\n    }\n\n    & .disabled {\n      cursor: not-allowed;\n      &:hover {\n        background: inherit;\n        color: inherit;\n      }\n    }\n  }\n\n  .dropdown-submenu:hover > span {\n    color: ", ";\n    background: ", ";\n  }\n"])), theme.textColor, theme.focus, theme.textColor, theme.focus); };
var DropdownLink = react_1.withTheme(function (_a) {
    var anchorRight = _a.anchorRight, anchorMiddle = _a.anchorMiddle, disabled = _a.disabled, title = _a.title, customTitle = _a.customTitle, caret = _a.caret, children = _a.children, menuClasses = _a.menuClasses, className = _a.className, alwaysRenderMenu = _a.alwaysRenderMenu, topLevelClasses = _a.topLevelClasses, theme = _a.theme, otherProps = tslib_1.__rest(_a, ["anchorRight", "anchorMiddle", "disabled", "title", "customTitle", "caret", "children", "menuClasses", "className", "alwaysRenderMenu", "topLevelClasses", "theme"]);
    return (<dropdownMenu_1.default alwaysRenderMenu={alwaysRenderMenu} {...otherProps}>
      {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var shouldRenderMenu = alwaysRenderMenu || isOpen;
            var cx = classnames_1.default('dropdown-actor', className, {
                'dropdown-menu-right': anchorRight,
                'dropdown-toggle': true,
                hover: isOpen,
                disabled: disabled,
            });
            var topLevelCx = classnames_1.default('dropdown', topLevelClasses, {
                'pull-right': anchorRight,
                'anchor-right': anchorRight,
                'anchor-middle': anchorMiddle,
                open: isOpen,
            });
            return (<span css={getRootCss(theme)} {...getRootProps({
                className: topLevelCx,
            })}>
            <a {...getActorProps({
                className: cx,
            })}>
              {customTitle || (<div className="dropdown-actor-title">
                  {title}
                  {caret && <icons_1.IconChevron direction={isOpen ? 'up' : 'down'} size="xs"/>}
                </div>)}
            </a>

            {shouldRenderMenu && (<ul {...getMenuProps({
                    className: classnames_1.default(menuClasses, 'dropdown-menu'),
                })}>
                {children}
              </ul>)}
          </span>);
        }}
    </dropdownMenu_1.default>);
});
DropdownLink.defaultProps = {
    alwaysRenderMenu: true,
    disabled: false,
    anchorRight: false,
    caret: true,
};
DropdownLink.displayName = 'DropdownLink';
exports.default = DropdownLink;
var templateObject_1;
//# sourceMappingURL=dropdownLink.jsx.map