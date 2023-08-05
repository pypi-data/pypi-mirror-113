Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var styles_1 = require("./styles");
var getTimeTooltipTitle = function (displayRelativeTime) {
    if (displayRelativeTime) {
        return locale_1.t('Switch to absolute');
    }
    return locale_1.t('Switch to relative');
};
var ListHeader = react_1.memo(function (_a) {
    var onSwitchTimeFormat = _a.onSwitchTimeFormat, displayRelativeTime = _a.displayRelativeTime;
    return (<react_1.Fragment>
    <StyledGridCell>{locale_1.t('Type')}</StyledGridCell>
    <Category>{locale_1.t('Category')}</Category>
    <StyledGridCell>{locale_1.t('Description')}</StyledGridCell>
    <StyledGridCell>{locale_1.t('Level')}</StyledGridCell>
    <Time onClick={onSwitchTimeFormat}>
      <tooltip_1.default title={getTimeTooltipTitle(displayRelativeTime)}>
        <StyledIconSwitch size="xs"/>
      </tooltip_1.default>
      <span> {locale_1.t('Time')}</span>
    </Time>
  </react_1.Fragment>);
});
exports.default = ListHeader;
var StyledGridCell = styled_1.default(styles_1.GridCell)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: sticky;\n  z-index: ", ";\n  top: 0;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  line-height: 1;\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n    font-size: ", ";\n  }\n"], ["\n  position: sticky;\n  z-index: ", ";\n  top: 0;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  line-height: 1;\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.zIndex.breadcrumbs.header; }, function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(2), space_1.default(2), function (p) { return p.theme.fontSizeSmall; });
var Category = styled_1.default(StyledGridCell)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var Time = styled_1.default(StyledGridCell)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: pointer;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: pointer;\n"])), space_1.default(1));
var StyledIconSwitch = styled_1.default(icons_1.IconSwitch)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  transition: 0.15s color;\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  transition: 0.15s color;\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=listHeader.jsx.map