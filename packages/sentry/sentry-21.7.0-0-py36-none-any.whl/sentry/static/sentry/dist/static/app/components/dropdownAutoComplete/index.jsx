Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var menu_1 = tslib_1.__importDefault(require("./menu"));
var DropdownAutoComplete = function (_a) {
    var _b = _a.allowActorToggle, allowActorToggle = _b === void 0 ? false : _b, children = _a.children, props = tslib_1.__rest(_a, ["allowActorToggle", "children"]);
    return (<menu_1.default {...props}>
    {function (renderProps) {
            var isOpen = renderProps.isOpen, actions = renderProps.actions, getActorProps = renderProps.getActorProps;
            // Don't pass `onClick` from `getActorProps`
            var _a = getActorProps(), _onClick = _a.onClick, actorProps = tslib_1.__rest(_a, ["onClick"]);
            return (<Actor isOpen={isOpen} role="button" tabIndex={0} onClick={isOpen && allowActorToggle ? actions.close : actions.open} {...actorProps}>
          {children(renderProps)}
        </Actor>);
        }}
  </menu_1.default>);
};
var Actor = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  /* This is needed to be able to cover dropdown menu so that it looks like one unit */\n  ", ";\n"], ["\n  position: relative;\n  width: 100%;\n  /* This is needed to be able to cover dropdown menu so that it looks like one unit */\n  ", ";\n"])), function (p) { return p.isOpen && "z-index: " + p.theme.zIndex.dropdownAutocomplete.actor; });
exports.default = DropdownAutoComplete;
var templateObject_1;
//# sourceMappingURL=index.jsx.map