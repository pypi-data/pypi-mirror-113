Object.defineProperty(exports, "__esModule", { value: true });
exports.MergedStyles = exports.ButtonGrid = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var button_1 = require("app/components/button");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function ButtonBar(_a) {
    var children = _a.children, className = _a.className, active = _a.active, _b = _a.merged, merged = _b === void 0 ? false : _b, _c = _a.gap, gap = _c === void 0 ? 0 : _c;
    var shouldCheckActive = typeof active !== 'undefined';
    return (<ButtonGrid merged={merged} gap={gap} className={className}>
      {!shouldCheckActive
            ? children
            : React.Children.map(children, function (child) {
                if (!React.isValidElement(child)) {
                    return child;
                }
                var childProps = child.props, childWithoutProps = tslib_1.__rest(child, ["props"]);
                // We do not want to pass `barId` to <Button>`
                var barId = childProps.barId, props = tslib_1.__rest(childProps, ["barId"]);
                var isActive = active === barId;
                // This ["primary"] could be customizable with a prop,
                // but let's just enforce one "active" type for now
                var priority = isActive ? 'primary' : childProps.priority || 'default';
                return React.cloneElement(childWithoutProps, tslib_1.__assign(tslib_1.__assign({}, props), { className: classnames_1.default(className, { active: isActive }), priority: priority }));
            })}
    </ButtonGrid>);
}
var MergedStyles = function () { return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* Raised buttons show borders on both sides. Useful to create pill bars */\n  & > .active {\n    z-index: 2;\n  }\n\n  & > .dropdown,\n  & > button,\n  & > a {\n    position: relative;\n\n    /* First button is square on the right side */\n    &:first-child:not(:last-child) {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-top-right-radius: 0;\n        border-bottom-right-radius: 0;\n      }\n    }\n\n    /* Middle buttons are square */\n    &:not(:last-child):not(:first-child) {\n      border-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-radius: 0;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    &:first-child {\n      & + .dropdown:not(:last-child),\n      & + a:not(:last-child),\n      & + button:not(:last-child) {\n        margin-left: -1px;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    /* stylelint-disable-next-line no-duplicate-selectors */\n    &:not(:last-child):not(:first-child) {\n      & + .dropdown,\n      & + button,\n      & + a {\n        margin-left: -1px;\n      }\n    }\n\n    /* Last button is square on the left side */\n    &:last-child:not(:first-child) {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n      margin-left: -1px;\n\n      & > .dropdown-actor > ", " {\n        border-top-left-radius: 0;\n        border-bottom-left-radius: 0;\n        margin-left: -1px;\n      }\n    }\n  }\n"], ["\n  /* Raised buttons show borders on both sides. Useful to create pill bars */\n  & > .active {\n    z-index: 2;\n  }\n\n  & > .dropdown,\n  & > button,\n  & > a {\n    position: relative;\n\n    /* First button is square on the right side */\n    &:first-child:not(:last-child) {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-top-right-radius: 0;\n        border-bottom-right-radius: 0;\n      }\n    }\n\n    /* Middle buttons are square */\n    &:not(:last-child):not(:first-child) {\n      border-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-radius: 0;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    &:first-child {\n      & + .dropdown:not(:last-child),\n      & + a:not(:last-child),\n      & + button:not(:last-child) {\n        margin-left: -1px;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    /* stylelint-disable-next-line no-duplicate-selectors */\n    &:not(:last-child):not(:first-child) {\n      & + .dropdown,\n      & + button,\n      & + a {\n        margin-left: -1px;\n      }\n    }\n\n    /* Last button is square on the left side */\n    &:last-child:not(:first-child) {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n      margin-left: -1px;\n\n      & > .dropdown-actor > ", " {\n        border-top-left-radius: 0;\n        border-bottom-left-radius: 0;\n        margin-left: -1px;\n      }\n    }\n  }\n"])), button_1.StyledButton, button_1.StyledButton, button_1.StyledButton); };
exports.MergedStyles = MergedStyles;
var ButtonGrid = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  ", "\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  ", "\n"])), function (p) { return space_1.default(p.gap); }, function (p) { return p.merged && MergedStyles; });
exports.ButtonGrid = ButtonGrid;
exports.default = ButtonBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=buttonBar.jsx.map