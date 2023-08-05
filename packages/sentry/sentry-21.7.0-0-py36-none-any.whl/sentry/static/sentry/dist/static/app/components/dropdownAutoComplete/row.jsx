Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Row(_a) {
    var item = _a.item, style = _a.style, itemSize = _a.itemSize, highlightedIndex = _a.highlightedIndex, inputValue = _a.inputValue, getItemProps = _a.getItemProps;
    var index = item.index;
    if (item === null || item === void 0 ? void 0 : item.groupLabel) {
        return (<LabelWithBorder style={style}>
        {item.label && <GroupLabel>{item.label}</GroupLabel>}
      </LabelWithBorder>);
    }
    return (<AutoCompleteItem itemSize={itemSize} isHighlighted={index === highlightedIndex} {...getItemProps({ item: item, index: index, style: style })}>
      {typeof item.label === 'function' ? item.label({ inputValue: inputValue }) : item.label}
    </AutoCompleteItem>);
}
exports.default = Row;
var getItemPaddingForSize = function (itemSize) {
    if (itemSize === 'small') {
        return space_1.default(0.5) + " " + space_1.default(1);
    }
    if (itemSize === 'zero') {
        return '0';
    }
    return space_1.default(1);
};
var LabelWithBorder = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  border-width: 1px 0;\n  color: ", ";\n  font-size: ", ";\n\n  :first-child {\n    border-top: none;\n  }\n  :last-child {\n    border-bottom: none;\n  }\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  border-width: 1px 0;\n  color: ", ";\n  font-size: ", ";\n\n  :first-child {\n    border-top: none;\n  }\n  :last-child {\n    border-bottom: none;\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
var GroupLabel = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n"], ["\n  padding: ", " ", ";\n"])), space_1.default(0.25), space_1.default(1));
var AutoCompleteItem = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  /* needed for virtualized lists that do not fill parent height */\n  /* e.g. breadcrumbs (org height > project, but want same fixed height for both) */\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  font-size: 0.9em;\n  background-color: ", ";\n  color: ", ";\n  padding: ", ";\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n\n  :last-child {\n    border-bottom: none;\n  }\n\n  :hover {\n    color: ", ";\n    background-color: ", ";\n  }\n"], ["\n  /* needed for virtualized lists that do not fill parent height */\n  /* e.g. breadcrumbs (org height > project, but want same fixed height for both) */\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  font-size: 0.9em;\n  background-color: ", ";\n  color: ", ";\n  padding: ", ";\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n\n  :last-child {\n    border-bottom: none;\n  }\n\n  :hover {\n    color: ", ";\n    background-color: ", ";\n  }\n"])), function (p) { return (p.isHighlighted ? p.theme.focus : 'transparent'); }, function (p) { return (p.isHighlighted ? p.theme.textColor : 'inherit'); }, function (p) { return getItemPaddingForSize(p.itemSize); }, function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.focus; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=row.jsx.map