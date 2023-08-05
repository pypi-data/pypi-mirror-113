Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var icons_1 = require("app/icons");
var ContextMenu = function (_a) {
    var children = _a.children;
    return (<dropdownMenu_1.default>
    {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var topLevelCx = classnames_1.default('dropdown', {
                'anchor-right': true,
                open: isOpen,
            });
            return (<MoreOptions {...getRootProps({
                className: topLevelCx,
            })}>
          <DropdownTarget {...getActorProps({
                onClick: function (event) {
                    event.stopPropagation();
                    event.preventDefault();
                },
            })}>
            <icons_1.IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={classnames_1.default('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
        }}
  </dropdownMenu_1.default>);
};
var MoreOptions = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: ", ";\n"], ["\n  display: flex;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var DropdownTarget = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  cursor: pointer;\n  padding: 0 5px;\n"], ["\n  display: flex;\n  cursor: pointer;\n  padding: 0 5px;\n"])));
exports.default = ContextMenu;
var templateObject_1, templateObject_2;
//# sourceMappingURL=contextMenu.jsx.map