Object.defineProperty(exports, "__esModule", { value: true });
exports.SingleEventHoverText = exports.ExternalDropdownLink = exports.ErrorNodeContent = exports.StyledTruncate = exports.DropdownItemSubContainer = exports.DropdownItem = exports.DropdownMenuHeader = exports.DropdownContainer = exports.TraceConnector = exports.EventNode = exports.QuickTraceContainer = exports.SectionSubtext = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var menuHeader_1 = tslib_1.__importDefault(require("app/components/actions/menuHeader"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var tag_1 = tslib_1.__importStar(require("app/components/tag"));
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
exports.SectionSubtext = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
exports.QuickTraceContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 24px;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 24px;\n"])));
var nodeColors = function (theme) { return ({
    error: {
        color: theme.white,
        background: theme.red300,
        border: theme.red300,
    },
    warning: {
        color: theme.red300,
        background: theme.background,
        border: theme.red300,
    },
    white: {
        color: theme.textColor,
        background: theme.background,
        border: theme.textColor,
    },
    black: {
        color: theme.background,
        background: theme.textColor,
        border: theme.textColor,
    },
}); };
exports.EventNode = styled_1.default(tag_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  span {\n    display: flex;\n    color: ", ";\n  }\n  & ", " {\n    background-color: ", ";\n    border: 1px solid ", ";\n  }\n"], ["\n  span {\n    display: flex;\n    color: ", ";\n  }\n  & " /* sc-selector */, " {\n    background-color: ", ";\n    border: 1px solid ", ";\n  }\n"])), function (p) { return nodeColors(p.theme)[p.type || 'white'].color; }, /* sc-selector */ tag_1.Background, function (p) { return nodeColors(p.theme)[p.type || 'white'].background; }, function (p) { return nodeColors(p.theme)[p.type || 'white'].border; });
exports.TraceConnector = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  width: ", ";\n  border-top: 1px solid ", ";\n"])), space_1.default(1), function (p) { return p.theme.textColor; });
/**
 * The DropdownLink component is styled directly with less and the way the
 * elements are laid out within means we can't apply any styles directly
 * using emotion. Instead, we wrap it all inside a span and indirectly
 * style it here.
 */
exports.DropdownContainer = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  .dropdown-menu {\n    padding: 0;\n  }\n"], ["\n  .dropdown-menu {\n    padding: 0;\n  }\n"])));
exports.DropdownMenuHeader = styled_1.default(menuHeader_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  ", ";\n  padding: ", " ", ";\n"], ["\n  background: ", ";\n  ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.first && 'border-radius: 2px'; }, space_1.default(1), space_1.default(1.5));
var StyledMenuItem = styled_1.default(menuItem_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  width: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return (p.width === 'large' ? '350px' : '200px'); }, function (p) { return p.theme.innerBorder; });
var MenuItemContent = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  width: 100%;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  width: 100%;\n"])));
function DropdownItem(_a) {
    var children = _a.children, onSelect = _a.onSelect, allowDefaultEvent = _a.allowDefaultEvent, to = _a.to, _b = _a.width, width = _b === void 0 ? 'large' : _b;
    return (<StyledMenuItem to={to} onSelect={onSelect} width={width} allowDefaultEvent={allowDefaultEvent}>
      <MenuItemContent>{children}</MenuItemContent>
    </StyledMenuItem>);
}
exports.DropdownItem = DropdownItem;
exports.DropdownItemSubContainer = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n\n  > a {\n    padding-left: 0 !important;\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n\n  > a {\n    padding-left: 0 !important;\n  }\n"])));
exports.StyledTruncate = styled_1.default(truncate_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  padding-left: ", ";\n  white-space: nowrap;\n"], ["\n  padding-left: ", ";\n  white-space: nowrap;\n"])), space_1.default(1));
exports.ErrorNodeContent = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, auto);\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, auto);\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(0.25));
exports.ExternalDropdownLink = styled_1.default(externalLink_1.default)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  display: inherit !important;\n  padding: 0 !important;\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: inherit !important;\n  padding: 0 !important;\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
function SingleEventHoverText(_a) {
    var event = _a.event;
    return (<div>
      <truncate_1.default value={event.transaction} maxLength={30} leftTrim trimRegex={/\.|\//g} expandable={false}/>
      <div>
        {formatters_1.getDuration(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)}
      </div>
    </div>);
}
exports.SingleEventHoverText = SingleEventHoverText;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=styles.jsx.map